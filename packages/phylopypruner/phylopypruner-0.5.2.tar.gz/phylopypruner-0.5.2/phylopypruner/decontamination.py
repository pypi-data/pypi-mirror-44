"Module for dealing with contamination-like issues."

from __future__ import print_function
from __future__ import absolute_import
import sys
import copy
import datetime
from collections import defaultdict
from itertools import combinations
from functools import partial
from multiprocessing import Pool
from multiprocessing import cpu_count
from phylopypruner import filtering
from phylopypruner.summary import Summary
from phylopypruner.prune_paralogs import prune_paralogs

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d")

def _exclude_and_rerun(taxon, summary, pruning_method, min_taxa, outgroup, dir_out):
    summary_copy = copy.deepcopy(summary)

    resample_summary = Summary()
    for log in summary_copy.logs:
        log_resampled = _resample(log, taxon, pruning_method, min_taxa,
                                    outgroup, dir_out)
        if log_resampled:
            resample_summary.logs.append(log_resampled)

    return resample_summary

def _resample(log, excluded, pruning_method, min_taxa, outgroup, dir_out):
    resample_log = copy.deepcopy(log)
    tree_excluded = filtering.exclude(resample_log.masked_tree, excluded)
    resample_log.msas_out = []
    if not tree_excluded:
        return None
    resample_log.settings.exclude = excluded
    resample_log.orthologs = prune_paralogs(pruning_method,
                                            tree_excluded,
                                            min_taxa,
                                            outgroup)
    resample_log.get_msas_out(dir_out)
    return resample_log

def jackknife(summary, dir_out, threads):
    """Exclude each OTUs within the summary, one by one, perform paralogy
    pruning and output summary statistics of the output alignments for each
    subsample.

    Parameters
    ----------
    summary : Summary object
        Perform paralogy pruning on the Log object's masked tree attribute, for
        each Log object within this Summary's logs attribute.
    dir_out : str
        Write the statistics for each case to the summary file within this
        directory.

    Returns
    -------
    None
    """
    taxa = summary.otus()
    total = len(taxa)
    resamples = set()
    # reuse the settings from the first log in the summary
    log = summary.logs[0]
    pruning_method = log.settings.prune
    min_taxa = log.settings.min_taxa
    outgroup = log.settings.outgroup
    pool = Pool(threads)

    part_jackknife = partial(
        _exclude_and_rerun, summary=copy.deepcopy(summary),
        pruning_method=pruning_method, min_taxa=min_taxa, outgroup=outgroup,
        dir_out=dir_out)

    for index, resample_summary in enumerate(
            pool.imap_unordered(part_jackknife, taxa), 1):
        print("{}==>{} jackknife resampling ({}/{} subsamples)".format(
            "\033[34m", "\033[0m", index, total), end="\r")
        sys.stdout.flush()
        resamples.add(resample_summary)
    pool.terminate()
    print("")

    for summary in resamples:
        excluded = summary.logs[0].settings.exclude[0]
        summary.report("{}_excluded".format(excluded), dir_out)

def _mean(data):
    """Returns the sample arithmetic mean of data. 0 is returned if an empty
    list was provided.

    Parameters
    ----------
    data : list of floats

    Returns
    _______
    out: float
        The sample arithmetic mean of data.
    """
    return float(sum(data)) / max(len(data), 1)

def _sdm(data):
    """Returns the squared deviations from the mean (SDM) of data.

    Parameters
    ----------
    data : list of floats

    Returns
    -------
    out : float
        The sum of square deviations of data.
    """
    return sum((x - _mean(data))**2 for x in data)

def _std(data):
    """Return the population standard deviation of data.

    Parameters
    ----------
    data : list of floats

    Returns
    -------
    out : float
        The population standard deviation of data.
    """
    if len(data) < 2:
        raise ValueError('variance requires at least two data points')
    return (_sdm(data) / len(data)) ** 0.5

def _rerun_wo_otu(log, otus, dir_out):
    log_copy = copy.deepcopy(log)
    pruning_method = log_copy.settings.prune
    min_taxa = log_copy.settings.min_taxa
    outgroup = log_copy.settings.outgroup
    tree = log_copy.masked_tree
    tree_excluded = filtering.exclude(tree, list(otus))
    log_copy.msas_out = []
    log_copy.settings.exclude = list(otus)
    if not tree_excluded:
        return None
    log_copy.orthologs = prune_paralogs(pruning_method,
                                        tree_excluded,
                                        min_taxa,
                                        outgroup)
    log_copy.get_msas_out(dir_out)
    return log_copy

def exclude_otus(summary, otus):
    """Exclude the provided OTUs from the provided Summary object.

    Parameters
    ----------
    summary : Summary object
        Prune MSAs from this summary.
    otus : list
        Remove the OTUs within this list from the Summary object.

    Returns
    -------
    summary : Summary object
        Input summary with the provided OTUs excluded.
    """
    for log in summary.logs:
        for msa in log.msas_out:
            for sequence in msa.sequences:
                if sequence.otu in otus:
                    msa.sequences.remove(sequence)

    return summary

def exclude_genes(summary, msas):
    """Exclude the multiple sequence alignments (MSAs) within the provided list
    from the provided Summary object.

    Parameters
    ----------
    summary : Summary object
        Prune MSAs from this summary.
    msas : list
        Remove the MultipleSequenceAlignment objects within this list from the
        Summary object.

    Returns
    -------
    summary : Summary object
        Input summary with the provided MSAs excluded.
    """
    for log in summary.logs:
        for msa in log.msas_out:
            if msa in msas:
                log.msas_out.remove(msa)

    return summary

def prune_by_exclusion(summary, otus, dir_out, threads):
    """Exclude the OTUs within the provided list of OTUs from the masked trees
    within summary, perform paralogy pruning and output statistics and
    alignments for each ortholog recovered.

    Parameters
    ----------
    summary : Summary object
        Prune masked trees within the logs of this summary.
    otus : list of strings
        Exclude OTUs within this list from the trees in the summary.
    dir_out : str
        Output statistics to this directory.

    Returns
    -------
    summary_out : Summary object
        A new summary that was generated after performing paralogy pruning on
        the masked trees within the input summary with the OTUs within the
        provided list removed.
    report : str
        Printable statistics of the summary_out

    Takes a Summary object, a list of OTUs and the path to the output directory
    as an input. Returns a new Summary object that is the summary after
    paralogy pruning with the OTUs within the list excluded.
    """
    # creating a copy of the summary prevents making changes to the trees in
    # that summary
    summary_copy = copy.deepcopy(summary)
    summary_out = Summary()
    alignments_count = len(summary_copy.logs)
    excluded_str = "output_{}".format("+".join(otu for otu in otus))
    excluded_str += "_excluded"

    part_rerun = partial(_rerun_wo_otu, otus=otus, dir_out=dir_out)
    pool = Pool(threads)

    for index, log_copy in enumerate(
            pool.imap_unordered(part_rerun, summary_copy.logs), 1):
    # for index, log in enumerate(summary_copy.logs, 1):
        print("{}==>{} paralogy pruning with OTUs removed ({}/{} trees)".format(
            "\033[34m", "\033[0m", index, alignments_count), end="\r")
        sys.stdout.flush()

        if log_copy:
            summary_out.logs.append(log_copy)

    pool.terminate()
    print("")
    report = summary_out.report(excluded_str, dir_out)

    return summary_out, report

def trim_freq_paralogs(factor, paralog_freq):
    """Returns a set of OTUs with a paralogy frequency that is factor times
    larger than the standard deviation of the paralogy frequency of all OTUs.

    Parameters
    ----------
    factor : float
        Set the threshold to be this float multiplied by the standard deviation
        of the paralogy frequency of all OTUs.
    paralog_freq : dictionary
        Paralogy frequency for each OTU, where key is OTU and paralogy
        frequency is value.

    Returns
    _______
    otus_above_threshold : list
        A set of OTUs with a paralogy frequency above the threshold.
    """
    threshold = _std(list(paralog_freq.values())) * factor
    otus_above_threshold = list()

    for otu in paralog_freq:
        if paralog_freq[otu] > threshold:
            otus_above_threshold.append(otu)

    if not otus_above_threshold:
        print("OTUs with high paralogy frequency: none")
        return otus_above_threshold

    print("OTUs with high paralogy frequency: " +
          ", ".join(otu for otu in otus_above_threshold))

    return otus_above_threshold

def trim_divergent(node, divergence_threshold=0.25, include=[]):
    """For each OTU with more than one sequence present in the provided node:
    calculate the ratio of the maximum pairwise distance of the sequences
    within the OTU compared to the average pairwise distance for that OTU
    compared to every other sequence. Delete every sequence from that OTU
    entirely if the ratio exceeds the divergence threshold.

    Parameters
    ----------
    node : TreeNode object
        The node that you want wish to delete divergent sequences from.
    divergence_threshold : float
        Divergence threshold in percent.

    Returns
    ------
    seqs_above_threshold : list
        List of OTUs above the established threshold.
    """
    # maximum pairwise distance within OTUs ({OTU: max_pdist})
    in_otus_max_dist = defaultdict(float)
    # pairwises pairwise distance between one OTU's sequences and other OTU's
    # sequences ({OTU: [dist_1, dist_2, ...]})
    out_otus_dists = defaultdict(list)
    # average pairwise distance between one OTU's sequences and another OTU's
    # sequences ({OTU: avg_pdist})
    out_otus_avg_dist = dict()
    # ratio between the maximum pairwise distance of the in-OTUs and the
    # average pairwise distance of the out-OTUs
    in_out_ratio = dict()
    otus_above_threshold = list()
    nodes_to_remove = set()
    otus_removed = 0

    for paralog in node.paralogs():
        for leaf in node.iter_leaves():
            if paralog is leaf:
                continue

            if paralog.otu() == leaf.otu():
                if (not in_otus_max_dist[paralog.otu()] or
                        paralog.distance_to(leaf) >
                        in_otus_max_dist[paralog.otu()]):
                    in_otus_max_dist[paralog.otu()] = paralog.distance_to(leaf)
            else:
                out_otus_dists[paralog.otu()].append(paralog.distance_to(leaf))

    for otu in out_otus_dists:
        out_otus_avg_dist[otu] = sum(out_otus_dists[otu]) / float(len(out_otus_dists[otu]))

    for otu in out_otus_avg_dist:
        in_out_ratio = in_otus_max_dist[otu] / out_otus_avg_dist[otu]
        if in_out_ratio > divergence_threshold:
            otus_above_threshold.append(otu)

    for leaf in node.iter_leaves():
        if leaf.otu() in otus_above_threshold:
            nodes_to_remove.add(leaf)
            otus_removed += 1

    if include:
        for otu in include:
            if otu in nodes_to_remove:
                nodes_to_remove.remove(otu)

    node.remove_nodes(nodes_to_remove)

    return otus_above_threshold

def discard_non_monophyly(nodes, taxonomic_groups):
    """Takes a list of TreeNode objects and a list of TaxonomicGroup objects as
    an input. Returns the subset of TreeNode objects where each taxonomic
    group, defined within the TaxonomicGroup objects, are recovered as
    monophyletic. Being monophyletic here means that no other OTU, than the
    defined OTUs within the group are present within each group.

    Parameters
    ----------
    nodes : list
      Check these TreeNode objects for monophyly.
    taxonomic groups : list
      A list of TaxonomicGroup objects.

    Returns
    -------
    monophyletic_nodes : list
      The subset of the input TreeNode objects which pass the test for
      monophyly.
    """
    otu_scores = defaultdict(int)

    for node in nodes:
        for group in taxonomic_groups:
            present_members = node.outgroups_present(group.otus)

            # Only consider cases where 2, or more, members are present.
            if not present_members:
                continue
            elif len(present_members) == 1:
                continue

            # Find the outermost node which contains all members of this group.
            largest_monophyly = None
            largest_polyphyly = None

            for branch in node.iter_branches():
                otus = set(branch.iter_otus())
                ingroups = branch.outgroups_present(present_members)
                outgroups = otus.difference(ingroups)
                outermost_otus = set()

                if len(ingroups) < 2:
                    continue
                elif len(outgroups) >= 2:
                    # Check whether all outgroups are part of a polytomy within
                    # the outermost node in this TreeNode object.
                    for child in branch.children:
                        if child.is_leaf():
                            outermost_otus.add(child.otu())

                    if not outgroups.issubset(outermost_otus):
                        continue

                    if len(ingroups) > len(largest_monophyly):
                        # Score +1 for monophyletic group but w. polytomies
                        pass

                if len(ingroups) == len(branch):
                    # The present members forms a monophyletic group.
                    if not largest_monophyly or len(branch) > len(largest_monophyly):
                        largest_monophyly= branch
                else:
                    # The present members do not form a monophyletic group.
                    if not largest_polyphyly or len(branch) > len(largest_polyphyly):
                        largest_polyphyly = branch

            # if not largest_monophyly or largest_polyphyly:
            #     continue

            # if not largest_monophyly or largest_polyphyly and (len(largest_polyphyly) - 1) > len(largest_monophyly):
            #     print(largest_polyphyly.view())

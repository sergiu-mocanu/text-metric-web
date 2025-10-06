import io
import contextlib
import signal
from enum import StrEnum

stderr = io.StringIO()
with contextlib.redirect_stderr(stderr):
    # Supress warning about missing installation of a deeplearning framework
    import evaluate as ev

from codebleu import calc_codebleu


class TextMetric(StrEnum):
    BL = 'bleu'
    CB = 'codebleu'
    RG = 'rouge'
    MT = 'meteor'
    CH = 'chrf'


def metric_to_title(metric: TextMetric = None):
    # Function that returns the name of a metric used in the confusion matrix representation
    title = ''
    match metric:
        case TextMetric.BL:
            title = 'BLEU'
        case TextMetric.CB:
            title = 'CodeBLEU'
        case TextMetric.RG:
            title = 'ROUGE'
        case TextMetric.MT:
            title = 'METEOR'
        case TextMetric.CH:
            title = 'ChrF'
    return title


# noinspection PyUnusedLocal
def timeout_handler(signum, frame):
    """Custom TimeOut exception used during CodeBLEU metric measurement.

    Due to CodeBLEU analyzing the AST of the input code, some AI-generated scripts with repetitive instructions lead
    to stack overflow during the metric measurement. The timeout limit avoids any undesired crashes.
    """
    raise TimeoutError('Execution timeout!')


# Initializing TimeOut exception
signal.signal(signal.SIGALRM, timeout_handler)


def calculate_metric(metric: TextMetric, baseline_script: str, ai_script: str) -> dict | float:
    """
    Measure the textual-similarity metric score between an AI-generated script and the humaneval baseline.

    Args:
        metric (TextMetric): textual-similarity metric
        baseline_script (str): humaneval baseline script
        ai_script (str): AI-generated script

    Returns:
        A dictionary containing the textual similarity score.
    """
    score = {}

    metric_calc = None
    if metric != TextMetric.CB:
        metric_calc = ev.load(str(metric.value))

    if not ai_script:
        if metric != TextMetric.CB:
            return 0.0
        else:
            return {"codebleu": 0.0,
                    "ngram_match_score": 0.0,
                    "weighted_ngram_match_score": 0.0,
                    "syntax_match_score": 0.0,
                    "dataflow_match_score": 0.0}

    if metric == TextMetric.CB:
        metric_complete = False
        signal.alarm(2)
        while not metric_complete:
            try:
                score = calc_codebleu(predictions=[ai_script], references=[baseline_script], lang='python')
                signal.alarm(0)
                metric_complete = True
            except TimeoutError:
                print('Timeout Error')
                signal.alarm(2)

    else:
        if metric == TextMetric.RG:
            results = metric_calc.compute(predictions=[ai_script], references=[baseline_script],
                                          rouge_types=['rougeL'])
        else:
            results = metric_calc.compute(predictions=[ai_script], references=[baseline_script])

        metric_name = metric.value

        if metric == TextMetric.RG:
            score = results['rougeL'].item()
        elif metric == TextMetric.MT:
            score = results[metric_name].item()
        elif metric == TextMetric.CH:
            score = results['score'] / 100
        else:
            score = results[metric_name]
    return score
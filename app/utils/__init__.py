"""
Helper Module Init
"""

import importlib
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))


from notebooks.utils import (  # noqa: E402
    plot_correlation_heatmap,
    plot_entries,
    plot_scatter_matrix,
    report_null_columns,
)

from .utils import load_data  # noqa: E402

importlib.reload(sys.modules["notebooks"])

__all__ = [
    "load_data",
    "plot_correlation_heatmap",
    "plot_entries",
    "plot_scatter_matrix",
    "report_null_columns",
]

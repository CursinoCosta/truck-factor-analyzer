"""Strategy implementations for truck factor estimation.

This package will contain pluggable strategies. Keep this file minimal
so tests and imports work during early development.
"""

from src.strategies.files import calculate_truck_factor_files, FileTruckFactorResult

__all__ = ["simple", "calculate_truck_factor_files", "FileTruckFactorResult"]
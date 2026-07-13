import os
from datetime import datetime


def create_results_dir(base_dir: str) -> str:
    """
    Create a directory to store results, named with the current timestamp.

    Parameters:
        base_dir : (str)
            The base directory for the results.

    Returns:
        results_dir : (str)
            Path to the created results' directory.

    Saves:
        A new directory within 'base_dir' named "results_YYYY-MM-DD_HH-MM-SS-ffffff".
    """

    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    results_dir_name = f"results_{timestamp}"
    results_dir = os.path.join(base_dir, results_dir_name)
    os.makedirs(results_dir)

    return results_dir


def create_dir(path: str) -> str:
    """
    Create a directory.

    Parameters:
        path : (str)
            The path of the directory.

    Returns:
        path : (str)
            The path of the directory.
    """

    os.makedirs(path, exist_ok=True)
    return path


def log_progress(
        current_step: int,
        total_steps: int,
        item_label: str,
        indent_level: int,
        empty_line: bool = False
) -> None:
    """
    Log a progress message to the console with a specific format.

    Parameters:
        current_step : (int)
            The current step.
        total_steps : (int)
            The total number of steps.
        item_label : (str)
            The label of the item being processed.
        indent_level : (int)
            The level of indentation (number of '#' characters).
        empty_line : (bool, optional)
            Whether to print an empty line before the progress log.
            Default is False.
    """

    prefix = "\n" if empty_line else ""
    print(f"{prefix}{indent_level * '#'} [{current_step}/{total_steps}] '{item_label}'")

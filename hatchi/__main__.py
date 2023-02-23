"""Main script for Hatchi library"""


def main(x_coord: float, y_coord: int) -> int:
    """Main function for the libray.
    Should be run as follows:

    ```python
    if __name__ == "__main__":
        main()
    ```
    """
    return x_coord + y_coord


if __name__ == "__main__":
    main(2, 3)

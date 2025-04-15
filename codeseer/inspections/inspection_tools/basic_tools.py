def get_the_coeff_part(coeff: float | int) -> str:
    """
    The function that gives the color that
    depended on coefficient of similarity.

    And returns it in format for html-report.
    """
    if coeff <= 50:
        return f"""<span class="green">{coeff}%</span>"""
    if coeff <= 80:
        return f"""<span class="orange">{coeff}%</span>"""
    return f"""<span class="red">{coeff}%</span>"""

"""Scenario registry that collects all scenarios from category modules."""

from ms.evals.scenarios.base import ScenarioDefinition


def get_all_scenarios() -> list[ScenarioDefinition]:
    """Collect all scenario definitions from all category modules.

    Returns:
        List of all scenario definitions across all categories and edge cases.
    """
    import ms.evals.scenarios.access_auth as access_auth
    import ms.evals.scenarios.data_storage as data_storage
    import ms.evals.scenarios.edge_cases as edge_cases
    import ms.evals.scenarios.general_inquiry as general_inquiry
    import ms.evals.scenarios.hardware as hardware
    import ms.evals.scenarios.network as network
    import ms.evals.scenarios.not_support as not_support
    import ms.evals.scenarios.security as security
    import ms.evals.scenarios.software as software

    all_scenarios: list[ScenarioDefinition] = []
    all_scenarios.extend(access_auth.get_scenarios())
    all_scenarios.extend(hardware.get_scenarios())
    all_scenarios.extend(network.get_scenarios())
    all_scenarios.extend(software.get_scenarios())
    all_scenarios.extend(security.get_scenarios())
    all_scenarios.extend(data_storage.get_scenarios())
    all_scenarios.extend(general_inquiry.get_scenarios())
    all_scenarios.extend(not_support.get_scenarios())
    all_scenarios.extend(edge_cases.get_scenarios())

    return all_scenarios

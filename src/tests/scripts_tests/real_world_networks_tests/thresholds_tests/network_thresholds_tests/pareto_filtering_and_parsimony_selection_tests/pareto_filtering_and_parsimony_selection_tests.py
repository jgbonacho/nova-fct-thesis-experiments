import unittest
from types import SimpleNamespace

from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThresholdName
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection import \
    pareto_filtering_and_parsimony_selection as pareto_module
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_plus_parsimony_selection_dataclass import \
    ParetoPlusParsimonySelection


class TestParetoFilteringAndParsimonySelection(unittest.TestCase):

    @staticmethod
    def _config():
        return SimpleNamespace(
            pareto_tolerance_fraction_modularity=0.10,
            pareto_tolerance_fraction_conductance=0.10,
            pareto_largest_community_fraction_boundary=0.80,
            pareto_singleton_or_near_singleton_fraction_boundary=0.30,
            pareto_tolerance_fraction_stability=0.10,
            pareto_null_model_z_score_boundary=1.96,
            pareto_null_model_p_value_boundary=0.05,
            pareto_null_model_rank_boundary=3
        )

    @staticmethod
    def _candidate(
            name=CandidateThresholdName.E_GLOBAL,
            value=0.20,
            modularity=0.50,
            conductance=0.30,
            k_predicted=2,
            largest_community_fraction=0.50,
            singleton_fraction=0.10,
            stability=0.70,
            acceptable_modularity=None,
            acceptable_conductance=None,
            acceptable_non_degenerate=None,
            acceptable_stability=None,
            modularity_z_score=2.50,
            modularity_p_value=0.02,
            modularity_rank=2,
            conductance_z_score=2.30,
            conductance_p_value=0.03,
            conductance_rank=2,
            acceptable_null_model=None,
            final_acceptable=False
    ):
        return SimpleNamespace(
            name=name,
            value=value,
            intrinsic_evaluation=SimpleNamespace(
                modularity=modularity,
                conductance=conductance,
                k_predicted=k_predicted,
                largest_community_fraction=largest_community_fraction,
                singleton_or_near_singleton_fraction=singleton_fraction,
                acceptable_modularity=acceptable_modularity,
                acceptable_conductance=acceptable_conductance,
                acceptable_non_degenerate=acceptable_non_degenerate
            ),
            stability_evaluation=SimpleNamespace(
                stability=stability,
                acceptable_stability=acceptable_stability
            ),
            null_model_evaluation=SimpleNamespace(
                modularity_z_score=modularity_z_score,
                modularity_empirical_p_value=modularity_p_value,
                modularity_rank=modularity_rank,
                conductance_z_score=conductance_z_score,
                conductance_empirical_p_value=conductance_p_value,
                conductance_rank=conductance_rank,
                acceptable_null_model=acceptable_null_model
            ),
            pareto_plus_parsimony_selection=SimpleNamespace(
                acceptable=final_acceptable
            )
        )

    def test_pareto_selection_dataclass_fieldnames_and_to_dict(self):
        selection = ParetoPlusParsimonySelection(acceptable=True)

        self.assertEqual(
            ParetoPlusParsimonySelection.fieldnames(),
            ["Acceptable?"]
        )
        self.assertEqual(
            selection.to_dict(),
            {"Acceptable?": True}
        )

    def test_check_modularity_uses_tolerance_range_and_inclusive_boundary(self):
        candidates = [
            self._candidate(modularity=1.00),
            self._candidate(modularity=0.20),
            self._candidate(modularity=0.00)
        ]
        config = self._config()
        config.pareto_tolerance_fraction_modularity = 0.80

        pareto_module._check_modularity(candidates, config)

        self.assertEqual(
            [
                candidate.intrinsic_evaluation.acceptable_modularity
                for candidate in candidates
            ],
            [True, True, False]
        )

        config.pareto_tolerance_fraction_modularity = 0.50
        pareto_module._check_modularity(candidates, config)

        self.assertEqual(
            [
                candidate.intrinsic_evaluation.acceptable_modularity
                for candidate in candidates
            ],
            [True, False, False]
        )

    def test_check_conductance_uses_tolerance_range_and_inclusive_boundary(self):
        candidates = [
            self._candidate(conductance=0.20),
            self._candidate(conductance=0.24),
            self._candidate(conductance=0.30)
        ]
        config = self._config()
        config.pareto_tolerance_fraction_conductance = 0.40

        pareto_module._check_conductance(candidates, config)

        self.assertEqual(
            [
                candidate.intrinsic_evaluation.acceptable_conductance
                for candidate in candidates
            ],
            [True, True, False]
        )

    def test_check_non_degenerate_uses_strict_boundaries(self):
        config = self._config()
        candidates = [
            self._candidate(
                k_predicted=2,
                largest_community_fraction=0.79,
                singleton_fraction=0.29
            ),
            self._candidate(
                k_predicted=1,
                largest_community_fraction=0.50,
                singleton_fraction=0.10
            ),
            self._candidate(
                k_predicted=2,
                largest_community_fraction=0.80,
                singleton_fraction=0.10
            ),
            self._candidate(
                k_predicted=2,
                largest_community_fraction=0.50,
                singleton_fraction=0.30
            )
        ]

        pareto_module._check_non_degenerate(candidates, config)

        self.assertEqual(
            [
                candidate.intrinsic_evaluation.acceptable_non_degenerate
                for candidate in candidates
            ],
            [True, False, False, False]
        )

    def test_check_stability_uses_tolerance_range(self):
        candidates = [
            self._candidate(stability=0.90),
            self._candidate(stability=0.86),
            self._candidate(stability=0.70)
        ]
        config = self._config()
        config.pareto_tolerance_fraction_stability = 0.25

        pareto_module._check_stability(candidates, config)

        self.assertEqual(
            [
                candidate.stability_evaluation.acceptable_stability
                for candidate in candidates
            ],
            [True, True, False]
        )

    def test_check_null_model_requires_all_modularity_and_conductance_evidence(self):
        config = self._config()
        candidates = [
            self._candidate(),
            self._candidate(modularity_z_score=None),
            self._candidate(conductance_p_value=0.06),
            self._candidate(
                modularity_z_score=1.96,
                modularity_p_value=0.05,
                modularity_rank=3,
                conductance_z_score=1.96,
                conductance_p_value=0.05,
                conductance_rank=3
            )
        ]

        pareto_module._check_null_model(candidates, config)

        self.assertEqual(
            [
                candidate.null_model_evaluation.acceptable_null_model
                for candidate in candidates
            ],
            [True, False, False, True]
        )

    def test_filter_acceptable_candidates_by_largest_threshold_and_keep_e_family(self):
        e_family = self._candidate(
            name=CandidateThresholdName.E_FAMILY,
            value=0.15,
            acceptable_modularity=False,
            acceptable_conductance=False
        )
        candidates = [
            e_family,
            self._candidate(
                name=CandidateThresholdName.E_GLOBAL,
                value=0.30,
                acceptable_modularity=True,
                acceptable_conductance=True
            ),
            self._candidate(
                name=CandidateThresholdName.E_ABOVE,
                value=0.40,
                acceptable_modularity=True,
                acceptable_conductance=True
            ),
            self._candidate(
                name=CandidateThresholdName.E_BELOW,
                value=0.20,
                acceptable_modularity=True,
                acceptable_conductance=True
            )
        ]

        filtered = (
            pareto_module.filter_candidate_thresholds_using_pareto_and_parsimony(
                candidate_thresholds=candidates,
                number_of_thresholds_to_retain=2,
                check_modularity=True,
                check_conductance=True
            )
        )

        self.assertEqual(
            [candidate.name for candidate in filtered],
            [
                CandidateThresholdName.E_ABOVE,
                CandidateThresholdName.E_GLOBAL,
                CandidateThresholdName.E_FAMILY
            ]
        )

    def test_filter_can_disable_e_family_retention(self):
        candidates = [
            self._candidate(
                name=CandidateThresholdName.E_FAMILY,
                value=0.10,
                acceptable_modularity=False
            ),
            self._candidate(
                name=CandidateThresholdName.E_GLOBAL,
                value=0.30,
                acceptable_modularity=True
            )
        ]

        filtered = (
            pareto_module.filter_candidate_thresholds_using_pareto_and_parsimony(
                candidate_thresholds=candidates,
                number_of_thresholds_to_retain=1,
                check_modularity=True,
                keep_e_family=False
            )
        )

        self.assertEqual(
            [candidate.name for candidate in filtered],
            [CandidateThresholdName.E_GLOBAL]
        )

    def test_filter_fallback_uses_documented_priority_order(self):
        candidates = [
            self._candidate(
                name=CandidateThresholdName.E_FAMILY,
                value=0.99,
                modularity=0.99,
                conductance=0.01,
                stability=0.99,
                acceptable_modularity=False,
                acceptable_conductance=False,
                acceptable_non_degenerate=False,
                acceptable_stability=False
            ),
            self._candidate(
                name=CandidateThresholdName.E_GLOBAL,
                value=0.20,
                modularity=0.80,
                conductance=0.50,
                stability=0.50,
                acceptable_modularity=False,
                acceptable_conductance=False,
                acceptable_non_degenerate=True,
                acceptable_stability=False
            ),
            self._candidate(
                name=CandidateThresholdName.E_BELOW,
                value=0.40,
                modularity=0.80,
                conductance=0.30,
                stability=0.40,
                acceptable_modularity=False,
                acceptable_conductance=False,
                acceptable_non_degenerate=True,
                acceptable_stability=False
            ),
            self._candidate(
                name=CandidateThresholdName.E_ABOVE,
                value=0.10,
                modularity=0.80,
                conductance=0.30,
                stability=0.90,
                acceptable_modularity=False,
                acceptable_conductance=False,
                acceptable_non_degenerate=True,
                acceptable_stability=False
            ),
            self._candidate(
                name=CandidateThresholdName.E_ELBOW,
                value=0.70,
                modularity=0.80,
                conductance=0.30,
                stability=0.90,
                acceptable_modularity=False,
                acceptable_conductance=False,
                acceptable_non_degenerate=True,
                acceptable_stability=False
            )
        ]

        filtered = (
            pareto_module.filter_candidate_thresholds_using_pareto_and_parsimony(
                candidate_thresholds=candidates,
                number_of_thresholds_to_retain=3,
                check_modularity=True,
                check_conductance=True,
                check_non_degenerate=True,
                check_stability=True,
                keep_e_family=False
            )
        )

        self.assertEqual(
            [candidate.name for candidate in filtered],
            [
                CandidateThresholdName.E_ELBOW,
                CandidateThresholdName.E_ABOVE,
                CandidateThresholdName.E_BELOW
            ]
        )

    def test_select_final_threshold_prefers_largest_acceptable_value(self):
        candidates = [
            self._candidate(
                name=CandidateThresholdName.E_GLOBAL,
                value=0.20,
                final_acceptable=True
            ),
            self._candidate(
                name=CandidateThresholdName.E_ABOVE,
                value=0.40,
                final_acceptable=True
            ),
            self._candidate(
                name=CandidateThresholdName.E_BELOW,
                value=0.30,
                final_acceptable=False
            )
        ]

        selected = (
            pareto_module.select_final_threshold_using_pareto_and_parsimony(
                candidates
            )
        )

        self.assertIs(selected, candidates[1])

    def test_select_final_threshold_retains_acceptable_e_family_with_same_k(self):
        e_family = self._candidate(
            name=CandidateThresholdName.E_FAMILY,
            value=0.20,
            k_predicted=3,
            final_acceptable=True
        )
        larger_candidate = self._candidate(
            name=CandidateThresholdName.E_ABOVE,
            value=0.50,
            k_predicted=3,
            final_acceptable=True
        )

        selected = (
            pareto_module.select_final_threshold_using_pareto_and_parsimony(
                [e_family, larger_candidate]
            )
        )

        self.assertIs(selected, e_family)

    def test_select_final_threshold_does_not_retain_e_family_with_different_k(self):
        e_family = self._candidate(
            name=CandidateThresholdName.E_FAMILY,
            value=0.20,
            k_predicted=2,
            final_acceptable=True
        )
        larger_candidate = self._candidate(
            name=CandidateThresholdName.E_ABOVE,
            value=0.50,
            k_predicted=3,
            final_acceptable=True
        )

        selected = (
            pareto_module.select_final_threshold_using_pareto_and_parsimony(
                [e_family, larger_candidate]
            )
        )

        self.assertIs(selected, larger_candidate)

    def test_select_final_threshold_fallback_uses_priority_order(self):
        candidates = [
            self._candidate(
                name=CandidateThresholdName.E_GLOBAL,
                value=0.80,
                modularity=0.95,
                conductance=0.05,
                stability=0.95,
                acceptable_non_degenerate=False,
                final_acceptable=False
            ),
            self._candidate(
                name=CandidateThresholdName.E_BELOW,
                value=0.20,
                modularity=0.70,
                conductance=0.30,
                stability=0.50,
                acceptable_non_degenerate=True,
                final_acceptable=False
            ),
            self._candidate(
                name=CandidateThresholdName.E_ABOVE,
                value=0.40,
                modularity=0.80,
                conductance=0.40,
                stability=0.90,
                acceptable_non_degenerate=True,
                final_acceptable=False
            )
        ]

        selected = (
            pareto_module.select_final_threshold_using_pareto_and_parsimony(
                candidates
            )
        )

        self.assertIs(selected, candidates[2])


if __name__ == "__main__":
    unittest.main()

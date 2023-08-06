=====
Usage
=====

To use fast-datacard in a project:

.. code:: bash

    fast-datacard datacard_config.yml

An example for a datacard and supporting dataframes can be found in the `examples/` folder.

datacards_config.yaml


.. code-block:: yaml

    general:
        analysis_name: CombinedHinv
        version: v1
        dataset: 2016
        luminosity: 35.9

    regions:
        regions:
          - Signal
          - SingleMu
          - DoubleMu

    data:
        data_names_df: Data
        input_df: examples/data/data_dummy.csv
        data_names_dc: data_obs

    signals:
        - name: VBF
          input_df: examples/data/VBF_dummy.csv

    backgrounds:
        - name: Ttw
          input_df: examples/data/backgrounds_dummy.csv
          regions:
            - Signal
        - name: Zinv
          input_df: examples/data/backgrounds_dummy.csv
          regions:
            - Signal
        - name: Qcd
          input_df: examples/data/backgrounds_dummy.csv
          regions:
            - Signal
        - name: Ewk
          input_df: examples/data/backgrounds_dummy.csv
          regions:
            - SingleMu
            - DoubleMu

    systematics:
        - name: lumiSyst
          type: lnN
          value: 1.026
          apply_to:
            - signals
          when: True
        - name: lumiSyst
          type: lnN
          value: 1.060
          apply_to:
            - Ewk
            - Zinv
          when: True

The config file specifies parameters like the luminosity (used to scale simulation), regions of interest, data & simulation inputs (signal/background) and systematic uncertainties (systematics).

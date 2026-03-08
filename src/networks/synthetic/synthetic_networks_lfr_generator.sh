#!/usr/bin/env bash

set -euo pipefail

# Clone and build the LFR Benchmark generator (see https://github.com/eXascaleInfolab/LFR-Benchmark_UndirWeightOvp).
echo "[INFO] Cloning LFR Benchmark generator"
git clone "https://github.com/eXascaleInfolab/LFR-Benchmark_UndirWeightOvp.git"
echo "[INFO] Building LFR Benchmark generator"
cd LFR-Benchmark_UndirWeightOvp
make
cd ..

# Define the parameters for the graphs.
list_n=(100 300)              # <--
list_d_avg=(20)
list_d_max=(50)
list_mu=(0.1 0.3)             # <--
list_t1=(2.0)
list_t2=(1.0)
list_c_min=(20)
list_c_max=(100)
list_on_percentages=(10 30)   # <--
list_om=(2 4)                 # <--

# Set the name of the network family.
network_family_name="F1"

# Set the number of instances per network.
t=2

# Loop over the parameter combinations and run the generator.
for n in "${list_n[@]}"; do
  for d_avg in "${list_d_avg[@]}"; do
    for d_max in "${list_d_max[@]}"; do
      for mu in "${list_mu[@]}"; do
        for t1 in "${list_t1[@]}"; do
          for t2 in "${list_t2[@]}"; do
            for c_min in "${list_c_min[@]}"; do
              for c_max in "${list_c_max[@]}"; do
                for on_percentage in "${list_on_percentages[@]}"; do
                  for om in "${list_om[@]}"; do

                    on=$(( n * on_percentage / 100 ))

                    out_dir="./${network_family_name}"
                    mkdir -p "$out_dir"
                    cd "$out_dir"

                    for instance in $(seq 1 "$t"); do
                      network_name="n${n}mu${mu}on${on}om${om}inst${instance}"
                      echo "[INFO] Generating LFR benchmark graph: ${network_name}"

                      if ! ../LFR-Benchmark_UndirWeightOvp/lfrbench_udwov \
                          -N "$n" -k "$d_avg" -maxk "$d_max" -mut "$mu" -t1 "$t1" -t2 "$t2" -minc "$c_min" -maxc "$c_max" \
                          -on "$on" -om "$om" \
                          -name "$network_name" \
                          -muw 0.1  # Required parameter, but not relevant for the experiments.
                      then
                        echo "[INFO] Continuing..."
                      fi
                    done

                    cd ..

                  done
                done
              done
            done
          done
        done
      done
    done
  done
done

# Remove the LFR Benchmark generator.
echo "[INFO] Cleaning up LFR Benchmark generator"
rm -rf LFR-Benchmark_UndirWeightOvp

echo "[INFO] Done"

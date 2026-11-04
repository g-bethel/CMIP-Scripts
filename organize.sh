
#!/bin/bash

module load nco

base_path="/quobyte/emoniergrp/CMIP5/esgf_cache/CMIP5/output1"
scenario="historical"
variable="tasmax"
ensemble="r1i1p1"

for institution_path in "$base_path"/*; do
    [[ -d "$institution_path" ]] || continue

    for model_path in "$institution_path"/*; do
        [[ -d "$model_path" ]] || continue

        for version_path in "$model_path"/"$scenario"/day/atmos/day/"$ensemble"/*; do
            [[ -d "$version_path" ]] || continue

            input_path="$version_path/$variable"
            [[ -d "$input_path" ]] || continue

            model=$(basename "$model_path")

            # Find and sort input NetCDF files
            files=("$input_path"/${variable}_day_${model}_${scenario}_${ensemble}_????????-????????.nc)
            [[ -f "${files[0]}" ]] || continue

            # Determine first and last dates
            first_file=$(basename "${files[0]}")
            last_file=$(basename "${files[-1]}")
            start_date=${first_file: -20:8}
            end_date=${last_file: -11:8}

            output_file="$input_path/${variable}_day_${model}_${scenario}_${ensemble}_${start_date}-${end_date}.nc"

            # Skip if output already exists
            if [[ -f "$output_file" ]]; then
                echo "Skipping (already exists): $output_file"
                continue
            fi

            echo "Processing: $model ($scenario, $variable, $ensemble)"
            echo "  Files: ${#files[@]}"
            echo "  Output: $output_file"

            if ncrcat -O "${files[@]}" "$output_file"; then
                echo "  Successfully created: $output_file"
            else
                echo "  ERROR: Failed to concatenate $model" >&2
                rm -f "$output_file"
            fi
        done
    done
done

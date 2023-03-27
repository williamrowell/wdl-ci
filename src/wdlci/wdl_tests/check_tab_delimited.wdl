version 1.0

# Check if file is tab-delimited
# Input type: File or GZ file

task check_tab_delimited {
	input {
		File current_run_output
		File validated_output
	}

	Int disk_size = ceil(size(current_run_output, "GB") + size(validated_output, "GB") + 50)
	String current_run_output_unzipped = sub(current_run_output, "\\.gz$", "")

	command <<<
		set -euo pipefail

		err() {
			message=$1

			echo -e "[ERROR] $message" >&2
		}

		if gzip -t ~{current_run_output}; then
			gzip -d ~{current_run_output} ~{validated_output}
		fi

		# Validated dir path in input block vs. command block is different
		validated_dir_path=$(dirname ~{validated_output})

		if ! awk '{exit !/\t/}' "${validated_dir_path}/$(basename ~{validated_output} .gz)"; then
			err "Validated file: [~{basename(validated_output)}] is not tab-delimited"
			exit 1
		else
			if awk '{exit !/\t/}' ~{current_run_output_unzipped}; then
				echo "Current run file: [~{basename(current_run_output)}] is tab-delimited"
			else
				err "Current run file: [~{basename(current_run_output)}] is not tab-delimited"
				exit 1
			fi
		fi
	>>>

	output {
	}

	runtime {
		docker: "ubuntu:xenial"
		cpu: 1
		memory: "3.75 GB"
		disk: disk_size + " GB"
		disks: "local-disk " + disk_size + " HDD"
		preemptible: 1
	}
}
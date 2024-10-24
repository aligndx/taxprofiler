process KRAKEN2_STATISTICS {
    tag "$kraken_report"
    label 'process_single'

    conda (params.enable_conda ? "conda-forge::python=3.8.3" : null)
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/python:3.8.3' :
        'quay.io/biocontainers/python:3.8.3' }"

    input:
    path kraken_report

    output:
    path '*.csv', emit: csv
    path "versions.yml", emit: versions

    when:
    task.ext.when == null || task.ext.when
    
    script:
    """
    calculate_statistics.py \
        $kraken_report \
        summary_statistics.csv

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version | sed 's/Python //g')
    END_VERSIONS
    """
}
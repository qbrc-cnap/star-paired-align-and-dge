task run_differential_expression {

    File sample_annotations
    File raw_count_matrix
    String base_group
    String experimental_group
    String output_deseq2_suffix
    String normalized_counts_suffix
    String versus_sep

    Int disk_size = 10

    String contrast_name = experimental_group + versus_sep + base_group
    String output_deseq2 = contrast_name + "." + output_deseq2_suffix
    String normalized_counts = contrast_name + "." + normalized_counts_suffix
    String output_figures_dir = contrast_name + "_figures"

    command <<<
        Rscript /opt/software/deseq2.R \
            ${raw_count_matrix} \
            ${sample_annotations} \
            ${base_group} \
            ${experimental_group} \
            ${output_deseq2} \
            ${normalized_counts}
        mkdir ${output_figures_dir}
        python3 /opt/software/make_dge_plots.py \
            -i ${output_deseq2} \
            -c ${normalized_counts} \
            -s ${sample_annotations} \
            -x ${contrast_name} \
            -o ${output_figures_dir}
    >>>

    output {
        File dge_table = "${output_deseq2}"
        File nc_table = "${normalized_counts}"
        Array[File] figures = glob("${output_figures_dir}/*")
    }  

    runtime {
        docker: "docker.io/blawney/star_rnaseq:v0.0.1"
        cpu: 2
        memory: "6 G"
        disks: "local-disk " + disk_size + " HDD"
        preemptible: 0
    }
}
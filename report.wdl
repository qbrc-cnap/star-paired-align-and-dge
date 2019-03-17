task generate_report {

    Array[String] r1_files
    Array[String] r2_files
    Array[File] deseq2_outputs
    File annotations
    String genome    
    String git_repo_url
    String git_commit_hash
    String normalized_counts_suffix
    String versus_sep

    Float adj_pval_threshold = 0.05

    Int disk_size = 10

    command <<<
        generate_report.py \
          -r1 ${sep=" " r1_files} \
          -r2 ${sep=" " r2_files} \
          -g "${genome}" \
          -r ${git_repo_url} \
          -c ${git_commit_hash} \
          -a ${annotations} \
          -d ${sep=" " deseq2_outputs} \
          -v ${versus_sep} \
          -p ${adj_pval_threshold} \
          -n ${normalized_counts_suffix} \
          -t /opt/report/report.md \
          -o completed_report.md

        pandoc -H /opt/report/report.css -s completed_report.md -o analysis_report.html
    >>>

    output {
        File report = "analysis_report.html"
    }

    runtime {
        docker: "docker.io/blawney/star_rnaseq:v0.0.1"
        cpu: 2
        memory: "6 G"
        disks: "local-disk " + disk_size + " HDD"
        preemptible: 0
    }
}
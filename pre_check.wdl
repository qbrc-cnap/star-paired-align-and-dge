workflow PairedRnaSeqAndDgeWorkflow {
    Array[File] r1_files
    Array[File] r2_files
    File sample_annotations
    Array[String] base_conditions
    Array[String] experimental_conditions
    String genome
    File star_index_path
    File gtf
    File bed_annotations
    String output_zip_name
    String git_repo_url
    String git_commit_hash

    call assert_valid {
        input:
            r1_files = r1_files,
            r2_files = r2_files,
            sample_annotations = sample_annotations,
            base_conditions = base_conditions,
            experimental_conditions = experimental_conditions
    }
}

task assert_valid {
    Array[File] r1_files
    Array[File] r2_files
    File sample_annotations
    Array[String] base_conditions
    Array[String] experimental_conditions

    command <<<
        # check that fastq files pass correctly:
    >>>
}
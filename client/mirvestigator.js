/**
 * @Program: miRvestigator
 * @Version: 2
 * @Author: Chris Plaisier
 * @Author: Christopher Bare
 * @Sponsored by:
 * Nitin Baliga, ISB
 * Institute for Systems Biology
 * 1441 North 34th Street
 * Seattle, Washington  98103-8904
 * (216) 732-2139
 * @Also Sponsored by:
 * Luxembourg Systems Biology Grant
 * 
 * If this program is used in your analysis please mention who
 * built it. Thanks. :-)
 * 
 * Copyright (C) 2010 by Institute for Systems Biology,
 * Seattle, Washington, USA.  All rights reserved.
 */

/**
 * get parameters for the current job and display them in the page.
 * if a callback function is given, call it when we're done.
 */
function getParameters(job_id, callback) {
  if (job_id) {
    jQuery.ajax({
      url: "/miRvestigator/parameters?id=" + job_id,
      context: document.body,
      dataType: "json",
      success: function(parameters) {
        $("#job_name").html(parameters.jobName);
        $("#job_id").html(job_id);
        $("#genes_submitted").html(parameters.genes_submitted);
        // if (parameters.annotated_sequences==0) {
        //   $("#annotated_sequences").html("Pending...");
        // }
        // else {
        $("#annotated_sequences").html(parameters.annotated_sequences);
        // }
        $("#motif_sizes").html(parameters.motif_sizes.join(", "));
        if (parameters.bgModel=="def") {
          $("#background_model").html("Default Weeder model");
        }
        else {
          $("#background_model").html("3' UTR specific model");
        }
        $("#seed_model").html(parameters.seed_model.join(", "));
        $("#model_wobble").html(parameters.model_wobble);
	$("#est_time").html("~" + estimate_running_time(parameters.annotated_sequences) + " minutes");
        if (callback)
            callback(parameters);
      },
      error: function(xmlHttpRequest, textStatus, errorThrown) {
        $("#job_name").html("<p>Error getting parameters: " + textStatus + "</p>");
        $("#output").append("<p>Error getting parameters: " + textStatus + "</p>");
      }
    });
  }
}

// estimate running time (to the nearest minute) based on the number of sequences
function estimate_running_time(n) {
    return Math.round((4 * n + 215) / 60);
}


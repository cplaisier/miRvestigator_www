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
        if (parameters.bgModel=="HS") {
          $("#background_model").html("Default Weeder model");
        }
        else {
          $("#background_model").html("3' UTR specific model");
        }
        $("#seed_model").html(parameters.seed_model.join(", "));
        $("#model_wobble").html(parameters.model_wobble);
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


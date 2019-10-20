var totalCounts;
var gradeCounts;
var subjectCounts;

$.ajax({
  url: "https://bamnit.com/api/listings/get_course_counts",
  async: false
}).done(function(res) {
  totalCounts = res['total_daily_count'];
  gradeCounts = res['grade_daily_count'];
  subjectCounts = res['subject_daily_count'];
});

// Helper functions to support 'getData' function
function addDays(date, days) {
  var newDate = new Date(date.valueOf());
  newDate.setDate(newDate.getDate() + days);
  return newDate;
}

function getDates(startDate, stopDate) {
  var dateArray = new Array();
  var currentDate = startDate;
  while (currentDate <= stopDate) {
    dateArray.push(new Date (currentDate));
    currentDate = addDays(currentDate, 1);
  }
  return dateArray;
}

function generateEmptyDateRange() {
  var today = new Date();
  var beginDate = addDays(today, -28);
  var endDate = addDays(today, 7);

  var dateRange = getDates(beginDate, endDate);
  for (var i = 0; i < dateRange.length; i++) {
    dateRange[i] = dateRange[i].toISOString().slice(0, 10);
  }
  var dates = {};
  for (const d of dateRange) {
    dates[d] = 0;
  }
  return dates;
}

function populateDateRange(data) {
  var dates = generateEmptyDateRange();
  for (const d of data) {
    dates[d[0]] = d[1];
  }
  return dates;
}



// Function to retrieve specific data to display
export function getData(target, lookupType) {
  let labels = [];
  let totalValues = [];
  let totalData = populateDateRange(totalCounts)
  for (const i of Object.entries(totalData)) {
    labels.push(i[0]);
    totalValues.push(i[1]);
  }

  let jobValues = [];
  let lookupDict = {
    'subject': subjectCounts,
    'grade': gradeCounts
  };
  let jobData = populateDateRange(lookupDict[lookupType][target]);
  for (const i of Object.entries(jobData)) {
    jobValues.push(i[1]);
  }

  let data = {
    labels: labels,
    totalValues: totalValues,
    jobValues: jobValues
  };

  return data;
}



// Get the total number of jobs for each classType
export function getClassTypeCounts() {
  const g = {};
  const s = {};

  const counts = {
    'grade': g,
    'subject': s
  };

  Object.entries(gradeCounts).map(function(x) {
    g[x[0]] = (x[1].map((y) => y[1]).reduce((a,b) => a + b, 0));
  });
  Object.entries(subjectCounts).map(function(x) {
    s[x[0]] = (x[1].map((y) => y[1]).reduce((a,b) => a + b, 0));
  });  

  return counts;
}



// Function to load all the course data into the App component state
export function loadCourseList(courseType) {
  const courseObject = (courseType == 'subject' ? subjectCounts : gradeCounts);
  return (
    Object.keys(courseObject).map(function(course) {
      return ({"name": course});
    })
  )
}

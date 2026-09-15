/**
 * Optional live Drive listing for the wedding site.
 *
 * 1. Open https://script.google.com
 * 2. New project → paste this file
 * 3. Deploy → New deployment → Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 4. Copy the Web app URL into DRIVE_LIST_URL in preshoot.html
 *
 * The folder must be shared with your Google account (or publicly viewable).
 */
function doGet() {
  var folderId = "1GckkRAYaA7xPZnm4rI3InbouSqPO77U9";
  var folder = DriveApp.getFolderById(folderId);
  var iterator = folder.getFiles();
  var files = [];

  while (iterator.hasNext()) {
    var file = iterator.next();
    var mime = file.getMimeType();
    var type = null;
    if (mime.indexOf("image/") === 0) type = "image";
    if (mime.indexOf("video/") === 0) type = "video";
    if (!type) continue;

    files.push({
      id: file.getId(),
      name: file.getName(),
      type: type,
      mime: mime,
    });
  }

  files.sort(function (a, b) {
    return a.name.localeCompare(b.name);
  });

  return ContentService.createTextOutput(
    JSON.stringify({
      folderId: folderId,
      updatedAt: new Date().toISOString(),
      files: files,
    })
  ).setMimeType(ContentService.MimeType.JSON);
}

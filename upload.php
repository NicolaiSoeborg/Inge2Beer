<?php
if ((!empty($_FILES["rusliste"])) && ($_FILES["rusliste"]['error'] == 0)) {
  $filename = basename($_FILES["rusliste"]['name']);
  $ext = substr($filename, strrpos($filename, '.') + 1);

  // Check file ext and size < 15 mb
  if (($ext == "xls") && ($_FILES["rusliste"]["size"] < 15000000)) {

      if (!is_dir("/tmp/uploads")) mkdir("/tmp/uploads");
      // Warning: newname _MUST_ to be hashed to protect 'exec'-call below.
      $newname = "/tmp/uploads/".md5($filename).'-'.time();
      //Check if the file with the same name is already exists on the server
      if (!file_exists($newname)) {

        //Attempt to move the uploaded file to it's new place
        if ((move_uploaded_file($_FILES["rusliste"]['tmp_name'], $newname))) {
           exec("/var/www/private/Inge2Beer/inge2beer.py ".$newname);
           exec("cd \"/tmp/uploads/\" && /usr/bin/timeout 5s /usr/bin/latex -interaction=nonstopmode \"".$newname.".tex\" 2> /dev/null");
           exec("cd \"/tmp/uploads/\" && /usr/bin/timeout 5s /usr/bin/dvips \"".$newname.".dvi\" 2> /dev/null");
           exec("cd \"/tmp/uploads/\" && /usr/bin/timeout 5s /usr/bin/ps2pdf \"".$newname.".ps\" 2> /dev/null");
           exec("cd \"/tmp/uploads/\" && rm \"".$newname.".aux\"");
           exec("cd \"/tmp/uploads/\" && rm \"".$newname.".dvi\"");
           exec("cd \"/tmp/uploads/\" && rm \"".$newname.".log\"");
           exec("cd \"/tmp/uploads/\" && rm \"".$newname.".ps\"");
           $z = new ZipArchive();
           if (!$z->open($newname.".zip", ZipArchive::CREATE))
             die("Can't create zip file.");
           $z->addFile("/var/www/private/Inge2Beer/templates/readme.txt", "README.txt");
           $z->addFile($newname.".pdf", "Barcodes.pdf");
           $z->addFile($newname.".tex", "Barcodes.tex");
           $z->addFile($newname.".db", "Beer.db");
           $z->addFile($newname.".sqlite3", "TEST-02350.sqlite3");
           $z->setArchiveComment("File generated ".date("Y-m-d H:i:s"));
           $z->close();
           $newname .= ".zip";
           header('Content-Type: application/octet-stream');
           header('Content-Disposition: attachment; filename="beer.zip"');
           header('Expires: 0');
           header('Cache-Control: must-revalidate');
           header('Content-Length: ' . filesize($newname));
           readfile($newname);
           unlink($newname);
           exit;
        } else {
           die("Error: A problem occurred during file upload!");
        }
      }
  } else {
     die("Error: Only .xls files under 15 MiB are accepted for upload.");
  }
} else {
 die("Error: No file uploaded.");
}
?>

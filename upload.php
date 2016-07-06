<?php
if ((!empty($_FILES["rusliste"])) && ($_FILES["rusliste"]['error'] == 0)) {
  $filename = basename($_FILES["rusliste"]['name']);
  $ext = substr($filename, strrpos($filename, '.') + 1);

  // Check file ext and size < 15 mb
  if (($ext == "xls") && ($_FILES["rusliste"]["size"] < 15000000)) {

      // Warning: newname _MUST_ to be hashed to protect 'exec'-call below.
      $newname = '/tmp/uploads/'.md5($filename).'-'.time();
      //Check if the file with the same name is already exists on the server
      if (!file_exists($newname)) {

        //Attempt to move the uploaded file to it's new place
        if ((move_uploaded_file($_FILES["rusliste"]['tmp_name'], $newname))) {
           exec("/tmp/Inge2Beer/inge2beer.py ".$newname);
           //exec("cd '/tmp/Inge2Beer/' && latex -interaction=batchmode ".$newname.".tex");
           //exec("cd '/tmp/Inge2Beer/' && dvips ".$newname.".dvi");
           //exec("cd '/tmp/Inge2Beer/' && ps2pdf ".$newname.".ps");

           exec("zip -j ".$newname.".zip ".$newname.".*");
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
           echo "Error: A problem occurred during file upload!";
        }
      }
  } else {
     echo "Error: Only .xls files under 15 MiB are accepted for upload.";
  }
} else {
 echo "Error: No file uploaded.";
}
?>

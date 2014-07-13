#!/usr/bin/env perl

BEGIN { push @INC, "$ENV{DOCUMENT_ROOT}/cgi-bin/admin/modules";}

use CGI qw(:standard);
my $q = new CGI;
use CGI::Carp qw(fatalsToBrowser);
require "$ENV{DOCUMENT_ROOT}/cgi-bin/library/functions.lib";

my $THIS = "http://$ENV{HTTP_HOST}";
my $THIS_SCRIPT = "/index.shtml";
my $THIS_CGI_SCRIPT = "$ENV{SCRIPT_NAME}";
my $created_file_folder = "$ENV{DOCUMENT_ROOT}/createdfiles"



# Routing
if ($q->param("action")) {
    eval "&" . $q->param("action");
} else {
    &index;
}

sub index() {
  
  print "Content-type: text/html\n\n";
  
  if ($q->param('re') == 1) {
    print qq~<p><b>The new file has been created.</b></p>
    ~;
  }
  print qq~<p>To create a file, enter the name of the file and the content.  The file will be creted as a text file</p>
  <form method="post" action="$THIS_CGI_SCRIPT">
  <input type="hidden" name="createfile" value="1"/>
  <p>Filename: <input type="text" name="filename" value="" size="10" /></p>
  <p>File Content: <br />
  <textarea name="filecontent" cols="40" rows="10"></textarea></p>
  <p><input type="submit" name="go" value="Create"/>
  </p>
  </form>
  ~;
  
print &file_list();
  
  
}


sub file_list {
  
  
            my @carts = ();
             my $cart_files;
               opendir (USER_CARTS, "$created_file_folder");
               @carts = grep(/\.txt/,readdir(USER_CARTS));
               closedir (USER_CARTS);
               
               
               foreach my $cart (@carts)
                 {
              $cart_files .= qq~<li><a href="/createdfiles/$cart">$cart</a></li>
              ~;
              }
            
            if ($cart_files) {
              return ("<ul>$cart_files</ul>");
            }
            else {
              return "";
            }
            
  
}

sub createfile {
  
  my $createfilename = &functions::FilterNeg($q->param('createfile'));
  $createfilename =~ s/[^a-z0-9]//gi;
  
  my $filecontent = &functions::FilterNeg($q->param('filecontent'));
  
  open (FILE, ">$created_file_folder/$createfilename\.txt");
  print FILE $filecontent;
  close(FILE);

print "Location: $THIS_URL$THIS_SCRIPT?re=1\n\n";  

}

1;
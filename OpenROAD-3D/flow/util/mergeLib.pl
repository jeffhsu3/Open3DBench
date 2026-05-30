#!/usr/bin/env perl

# This script is sourced from Brown (with modifications). It merges
# several timing libraries into one, making sure templates are not lost.
# ------------------------------------------------------------------------------

use strict;
use warnings;

my $sclname = $ARGV[0];
shift @ARGV;
my $cnt = @ARGV;

if($cnt>0){
  process_header($ARGV[0]);
  
  # Extract and print all unique templates from all files
  my %templates;
  foreach my $file (@ARGV) {
      extract_templates($file, \%templates);
  }
  foreach my $name (sort keys %templates) {
      print $templates{$name};
  }

  foreach my $file (@ARGV) {
      process_cells($file);
  }
  print "\n}\n";
} else {
  print "use: mergeLib.pl new_library_name lib1 lib2 lib3 ....";
}


sub process_header {
  my $filename  = shift;
  open(my $fh, '<', $filename) or die "Could not open file $filename $!";
  while (<$fh>) {
    if(/library\s*\(/) {
      print "library ($sclname) {\n";
      next;
    }
    last if(/^[\t\s]*(cell|lu_table_template|power_lut_template)\s*\(/);
    print $_;
  }
  close($fh);
}

sub extract_templates {
  my $filename = shift;
  my $templates_ref = shift;
  open(my $fh, '<', $filename) or die "Could not open file $filename $!";
  my $in_template = 0;
  my $template_name = "";
  my $template_content = "";
  my $brace_depth = 0;
  while (my $line = <$fh>) {
    if (!$in_template) {
      if ($line =~ /^\s*(lu_table_template|power_lut_template)\s*\(\s*([^\)]+)\s*\)/) {
        $in_template = 1;
        $template_name = $2;
        $template_content = $line;
        $brace_depth = 0;
        $brace_depth++ while $line =~ /\{/g;
        $brace_depth-- while $line =~ /\}/g;
        if ($brace_depth == 0) {
          $templates_ref->{$template_name} = $template_content;
          $in_template = 0;
        }
      }
    } else {
      $template_content .= $line;
      $brace_depth++ while $line =~ /\{/g;
      $brace_depth-- while $line =~ /\}/g;
      if ($brace_depth <= 0) {
        $templates_ref->{$template_name} = $template_content;
        $in_template = 0;
      }
    }
  }
  close($fh);
}

sub process_cells {
  my $filename  = shift;

  open(my $fh, '<', $filename) or die "Could not open file $filename $!";

  my $flag = 0;
  # cut the cells
  while (<$fh>) {
    #chomp $_;
    if(/^[\t\s]*cell\s*\(/) {#&& $flag==0){
      die "Error! new cell before finishing the previous one!\n" if($flag!=0);
      print "\n$_";
      $flag=1;
    } elsif($flag > 0){
      $flag++ if(/\{/);
      $flag-- if(/\}/);
      #print "...}\n" if($flag==0);
      print "$_";
    }
  }
  close($fh);
}

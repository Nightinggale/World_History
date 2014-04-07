#!/usr/bin/perl -w

# tag extractor
# written by Trade Winds

#looks for a tag in my $text = 'HERE_';
#and pushes them into file2.txt

use strict;

my $text = 'UNITCLASS_';


open(FILE, "CIV4CivicInfos.xml") || die "File not found";

my @newlines;
my @writer;
my %hash;
@hash{@newlines}=();

while (<FILE>) {
 	#chomp;
	my $line = $_;

		if ($line =~ /$text/) {

			if($line =~ m/$text(\w+)/) {
				
				if (exists($hash{$1})) # Here, I wanted to avoid including existing tags, but I can't yet. Monkey nature!!!
						{
  						print "yes";
						} 
					else 
						{
  						push(@newlines,"'$1',");
						@hash{@newlines}=();
						}

			
			
			}
		}

 }

close (FILE); 

open(FILE, ">file2.txt") || die "File not found";
print FILE @newlines;
close(FILE);

print "Done in file2.txt";
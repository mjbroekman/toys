#!/usr/bin/env perl

# Item-finder

use Data::Dumper;
use Getopt::Long;

sub bycost { $items{$a}{cost} <=> $items{$b}{cost}; }
sub byqty { $items{$a}{max} <=> $items{$b}{max}; }

sub getmax { return int($_[0] / $_[1] ); }
sub get_total {
  my ( %items ) = @_;
  my $sum = 0;
  foreach my $i ( keys %items ) {
    $sum += $items{$i}{qty} * $items{$i}{cost}
  }
  return $sum;
}

sub createhash {
  my %items;
  $items{"yoyo"}{cost} = 1.22;
  $items{"doll"}{cost} = 2.75;
  $items{"duckie"}{cost} = 1.85;
  $items{"tractor"}{cost} = 5.97;
  $items{"airplane"}{cost} = 6.47;
  $items{"ball"}{cost} = 2.16;
  $items{"racecar"}{cost} = 7.13;
  $items{"dog"}{cost} = 4.57;
  $items{"jumprope"}{cost} = 1.46;
  $items{"car"}{cost} = 5.18;
  $items{"elephant"}{cost} = 3.16;
  $items{"bear"}{cost} = 4.89;
  $items{"xylophone"}{cost} = 7.11;
  $items{"tank"}{cost} = 6.45;
  $items{"checkers"}{cost} = 4.77;
  $items{"boat"}{cost} = 8.04;
  $items{"train"}{cost} = 6.71;
  $items{"jacks"}{cost} = 2.31;
  $items{"truck"}{cost} = 6.21;
  $items{"whistle"}{cost} = 0.98;
  $items{"pinwheel"}{cost} = 0.87;
  return %items;
}
my $total = 0;
my $defaults = 0;

&GetOptions(
            "total=f" => \$total,
            "defaults" => \$defaults,
           );

if ( $total == 0 ) {
  print "Enter desired total: ";
  $total = <STDIN>;
  chomp $total;
  die("You are looking for a negative amount of money as a total. Not possible\n") if ( $total < 0 );
}
my $i_cost = "0";
my %items;
my %saved;
if ( $defaults ) {
  %items = createhash();
} else {
  while ( $i_cost ne "q" ) {
    print "Enter item name (q to finish): ";
    my $i_name = <STDIN>;
    chomp $i_name;
    $i_cost = "q" and next if ( $i_name eq "q" );
    print "Enter item cost (q to finish): ";
    $i_cost = <STDIN>;
    chomp $i_cost;
    $items{$i_name}{cost} = $i_cost if ( $i_cost > 0 and $i_cost ne "q" );
    $saved{$i_name}{cost} = $i_cost if ( $i_cost > 0 and $i_cost ne "q" );
  }
}

# print "Searching the following items for combinations totalling $total:\n";
foreach my $key ( keys %items ) {
   $items{$key}{max} = getmax($total,$items{$key}{cost});
#   print "\t$key (Cost: \$$items{$key}{cost}/ea)\n";
   $items{$key}{qty} = 0;
}
# print "\n";

# A B C D E F G H I J K L M   TOTAL
# 0 0 0 0 0 0 0 0 0 0 0 0 0   0
# 1 0 0 0 0 0 0 0 0 0 0 0 0   1
printf("%10s " x scalar(keys %items), sort { $items{$b}{cost} <=> $items{$a}{cost} } keys %items);
printf("%10s\n", "Total");
sub print_row {
  my $row = "";
  foreach my $key ( sort { $items{$b}{cost} <=> $items{$a}{cost} } keys %items ) {
    $row .= sprintf("%10d ", $items{$key}{qty});
  }
  $row .= sprintf("%10.2f", get_total(%items));
  return $row;
}

print print_row . "\n";
sub change {
    my ($cset, $amt) = @_;
    if ($amt == 0)    { return [] }
    if (@$cset == 0)  { return "" }
    my $coin = shift @$cset;
    if ($coin > $amt) {
      print "$coin > $amt\n";
      $coin=change($cset, $amt);
      return$coin if!ref$coin;
      return[$coin];
    }
    else {
      print "Checking $amt - $coin\n";
      my $rval =change( [$coin, @$cset], $amt - $coin );
      return[$coin, @{$rval}]if ref $rval;
      print "Exception forces backing up to $amt\n";
      return [@{change($cset, $amt)}];
    }
}

sub subset_sum {
  my ( $total, @)
}
my @item_list = sort { $items{$b}{cost} <=> $items{$a}{cost} } keys %items;
my $t_sum = 0;
ITEM: foreach my $item ( @item_list ) {
  $items{$item}{qty}++;
  if ( $items{$item}{qty} > $items{$item}{max} ) {
    $items{$item}{qty} = 0;
    next ITEM;
  }
  ADDON: foreach my $addon ( @item_list ) {
    next ADDON if ( $item eq $addon );
    while ( $items{$addon}{qty} < $items{$addon}{max} ) {
      $items{$addon}{qty}++;
      print print_row;
      if ( get_total(%items) == $total ) {
        print " !!!!!\n";
      } else {
        print " xxxxx\n";
      }
    }
    $items{$addon}{qty} = 0;
  }
}
exit;
    # foreach my $key ( keys %items ) {
    #   next if ( $key eq $item );
    #   $items{$key}{max} = getmax($total,$items{$key}{cost});
    #   $items{$key}{qty} = 0;
    # }
    # $t_sum = get_total(%items);
    # if ( $t_sum > $total ) {
    #   $items{$item}{qty}--;
    #   $t_sum -= $items{$item}{cost};
    #   next ITEM;
    # }
#     ADDON: foreach my $addon ( sort { $items{$b}{cost} <=> $items{$a}{cost} } keys %items ) {
#       next if ( $item eq $addon );
#       INCR: while ($items{$addon}{qty} < $items{$addon}{max} && $t_sum < $total) {
#         $items{$addon}{qty}++;
#         $t_sum = get_total(%items);
#         if ( $t_sum > $total ) {
#           $items{$addon}{qty}--;
#           $t_sum -= $items{$addon}{cost};
#           next ADDON;
#         }
#         if ( $t_sum == $total ) {
#           last LOOP;
#         }
#       }
#     }
#     foreach my $i ( keys %items ) {
#       if ( $items{$i}{qty} > 0 ) {
#         next if ( $i eq $item );
#         $items{$i}{qty}--;
#         $items{$i}{max}--;
#       }
#     }
#   }
# }
#
# my $result = "";
# foreach my $i ( sort {
#     $items{$b}{qty} <=> $items{$a}{qty}
#       or
#     $a cmp $b
#   } keys %items ) {
#   if ( $items{$i}{qty} > 0 ) {
#     $result .= " $items{$i}{qty} $i @ $items{$i}{cost}\t+";
#   }
# }
# $result =~ s/ \+$//;
# print "$result\t= $t_sum\n";
#
# $t_sum = 0;
# foreach my $i ( keys %items ) {
#   delete $items{$i};
# }
#
# if ( $defaults ) {
#   %items = createhash();
# } else {
#   %items = %saved;
# }
#
# goto LOOP;

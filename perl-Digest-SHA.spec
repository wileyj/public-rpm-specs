%define cpan_name Digest::SHA
%define pkgname Digest-SHA
%define cpan_version %(echo `curl -s https://metacpan.org/pod/%{cpan_name} | grep "Module version" | cut -d":" -f2`)
%define filelist %{pkgname}-%{version}-filelist


name:      perl-Digest-SHA
summary:   Digest-SHA - Perl extension for SHA-1/224/256/384/512
version: %{cpan_version}
release:   1.%{dist}
license:   Artistic
Vendor: %{vendor}
Packager: %{packager}
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
buildarch: x86_64
prefix:    %(echo %{_prefix})
BuildRequires: perl-srpm-macros

Provides: %{name}
%{?load: %{_sourcedir}/macros.perl}


%description
Digest::SHA is written in C for speed.  If your platform lacks a
C compiler, you can install the functionally equivalent (but much
slower) the Digest::SHA::PurePerl manpage module.

The programming interface is easy to use: it's the same one found
in CPAN's the Digest manpage module.  So, if your applications currently
use the Digest::MD5 manpage and you'd prefer the stronger security of SHA,
it's a simple matter to convert them.

The interface provides two ways to calculate digests:  all-at-once,
or in stages.  To illustrate, the following short program computes
the SHA-256 digest of "hello world" using each approach:

	use Digest::SHA qw(sha256_hex);

	$data = "hello world";
	@frags = split(//, $data);

	# all-at-once (Functional style)
	$digest1 = sha256_hex($data);

	# in-stages (OOP style)
	$state = Digest::SHA->new(256);
	for (@frags) { $state->add($_) }
	$digest2 = $state->hexdigest;

	print $digest1 eq $digest2 ?
		"whew!\n" : "oops!\n";

To calculate the digest of an n-bit message where *n* is not a
multiple of 8, use the *add_bits()* method.  For example, consider
the 446-bit message consisting of the bit-string "110" repeated
148 times, followed by "11".  Here's how to display its SHA-1
digest:

	use Digest::SHA;
	$bits = "110" x 148 . "11";
	$sha = Digest::SHA->new(1)->add_bits($bits);
	print $sha->hexdigest, "\n";

Note that for larger bit-strings, it's more efficient to use the
two-argument version *add_bits($data, $nbits)*, where *$data* is
in the customary packed binary format used for Perl strings.

The module also lets you save intermediate SHA states to a string.  The
*getstate()* method generates portable, human-readable text describing
the current state of computation.  You can subsequently restore that
state with *putstate()* to resume where the calculation left off.

To see what a state description looks like, just run the following:

	use Digest::SHA;
	print Digest::SHA->new->add("Shaw" x 1962)->getstate;

As an added convenience, the Digest::SHA module offers routines to
calculate keyed hashes using the HMAC-SHA-1/224/256/384/512
algorithms.  These services exist in functional form only, and
mimic the style and behavior of the *sha()*, *sha_hex()*, and
*sha_base64()* functions.

	# Test vector from draft-ietf-ipsec-ciph-sha-256-01.txt

	use Digest::SHA qw(hmac_sha256_hex);
	print hmac_sha256_hex("Hi There", chr(0x0b) x 32), "\n";

%prep
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s https://metacpan.org/pod/%{cpan_name} | grep "tar.gz" | cut -d '"' -f2`
tar -xzvf $RPM_SOURCE_DIR/%{name}.tar.gz
#%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
cd $RPM_BUILD_DIR/%{pkgname}-%{cpan_version}
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '`
echo "Y" | %{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}" 

%install
cd $RPM_BUILD_DIR/%{pkgname}-%{cpan_version}
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

cmd=/usr/share/spec-helper/compress_files
[ -x $cmd ] || cmd=/usr/lib/rpm/brp-compress
[ -x $cmd ] && $cmd

# SuSE Linux
if [ -e /etc/SuSE-release -o -e /etc/UnitedLinux-release ]
then
    %{__mkdir_p} %{buildroot}/var/adm/perl-modules
    %{__cat} `find %{buildroot} -name "perllocal.pod"`  \
        | %{__sed} -e s+%{buildroot}++g                 \
        > %{buildroot}/var/adm/perl-modules/%{name}
fi

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null

%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    #print "%doc  src Changes examples README";
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
        }
    print join "\n", sort @ret;

    sub wanted {
        return if /auto$/;

        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;

        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;

        $dirs[@dirs] = $_;
        }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
        }
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files -f %{pkgname}-%{cpan_version}/%filelist
%defattr(-,root,root)

%changelog
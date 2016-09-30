%define pkgname cpan2rpm
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 0

name:      cpan2rpm
summary:   cpan2rpm - A Perl module packager
version:   2.028
release:   1.%{dist}
Vendor: %{vendor}
Packager: %{packager}
license:   Gnu Public License (GPL)
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
prefix:    %(echo %{_prefix})
requires:  %([ -e /etc/SuSE-release -o -e /etc/UnitedLinux-release ] && SuSE=1;ver=`rpm -q rpm --qf %%{version}|awk -F . '{print $1}'`;[ $ver -le 3 -o -n "$SuSE" ] && echo rpm || echo rpm-build)
BuildRequires: perl-libwww-perl, perl-HTTP-Tiny
Requires: perl-libwww-perl, perl-HTTP-Tiny
source:    cpan2rpm-2.028.tar.gz
buildarch: x86_64
BuildRequires: perl, perl-devel, perl-libs, perl-ExtUtils-MakeMaker, perl-Pod-Parser

%description
This script generates an RPM package from a Perl module.  It uses the standard RPM file structure and creates a spec file, a source RPM, and a binary, leaving these in their respective directories.
The script can operate on local files, directories, urls and CPAN module names.  Install this package if you want to create RPMs out of Perl modules.
The syntax for cpan2rpm supports multiple *distribution* names, which can take one of four different forms:
	1. a CPAN module name (e.g. XML::Simple) - When a module name is passed, the script will "walk" search.cpan.org to determine the latest distribution.  
	2. a URL (both http:// and ftp:// style locators will work) - In this and the above case, an automatic download of the needed tarball is performed (see notes for how).  The tarball is deposited in the SOURCES directory.
	3. a path to a tarball (e.g. /tmp/XML-Simple-1.05.tar.gz) - In this case, the tarball indicated gets copied to the SOURCES directory.
	4. a directory path - The directory specified must contain a Makefile.PL.  If the user intends to build a package from a directory (i.e. user does NOT specify --spec-only), the commands:
    perl Makefile.PL
    make
    make dist
will be performed in that directory in order to create the tarball necessary for package creation.


#
# This package was generated automatically with the cpan2rpm
# utility.  To get this software or for more information
# please visit: http://perl.arix.com/
#

%prep
%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
perl -pi -e 's/Pod::Text/Pod::PlainText/' "cpan2rpm"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '`
%{__make} 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

cmd=/usr/share/spec-helper/compress_files
[ -x $cmd ] || cmd=/usr/lib/rpm/brp-compress
[ -x $cmd ] && $cmd

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
    print "%doc perl.req.patch Changes README.redhat6 LICENSE README";
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

%files -f %filelist
%defattr(-,root,root)

%changelog

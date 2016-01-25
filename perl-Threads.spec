%define cpan_name threads
%define pkgname threads
%define cpan_version %(echo `curl -s https://metacpan.org/pod/%{cpan_name} | grep "Module version" | awk {'print $4'} |tr -d 'itemprop="softwareVersion"></span>'`)
%define filelist %{pkgname}-%{version}-filelist

Name:           perl-threads
Epoch:          1
version: %{cpan_version}
Release:        2.%{dist}
Summary:        Perl interpreter-based threads
License:        GPL+ or Artistic
Packager: %{packager}
Vendor: %{vendor}
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/threads/
BuildRequires:  perl,perl-srpm-macros
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(overload)
BuildRequires:  perl(XSLoader)
# Tests only:
BuildRequires:  perl(ExtUtils::testlib)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Hash::Util)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Thread::Queue)
BuildRequires:  perl(Thread::Semaphore)
BuildRequires:  perl(threads::shared)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Provides: %{name}
%{?load: %{_sourcedir}/macros.perl}


%description
Since Perl 5.8, thread programming has been available using a model called
interpreter threads which provides a new Perl interpreter for each thread,
and, by default, results in no data or state information being shared
between threads.

(Prior to Perl 5.8, 5005threads was available through the "Thread.pm" API.
This threading model has been deprecated, and was removed as of Perl 5.10.0.)

%prep
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s https://metacpan.org/pod/%{cpan_name} | grep "tar.gz" | cut -d '"' -f4`
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

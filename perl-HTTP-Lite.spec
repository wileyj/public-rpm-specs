%define cpan_name HTTP::Lite
%define pkgname HTTP-Lite
%define cpan_version %(echo `curl -s https://metacpan.org/pod/%{cpan_name} | grep "Module version" | awk {'print $4'} |tr -d 'itemprop="softwareVersion"></span>'`)
%define filelist %{pkgname}-%{version}-filelist

name:      perl-HTTP-Lite
summary:   HTTP-Lite - Lightweight HTTP implementation
version: %{cpan_version}
release:   1.%{dist}
license:   Artistic
Vendor: %{vendor}
Packager: %{packager}
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
prefix:    %(echo %{_prefix})
BuildRequires: perl, perl-srpm-macros,  perl-devel, perl-libs, perl-ExtUtils-MakeMaker


Provides: %{name}
%{?load: %{_sourcedir}/macros.perl}


%description
HTTP::Lite is a stand-alone lightweight HTTP/1.1 implementation
    for perl.  It is not intended as a replacement for the
    fully-features LWP module.  Instead, it is intended for use in
    situations where it is desirable to install the minimal number of
    modules to achieve HTTP support, or where LWP is not a good
    candidate due to CPU overhead, such as slower processors.
    HTTP::Lite is also significantly faster than LWP.

    HTTP::Lite is ideal for CGI (or mod_perl) programs or for bundling
    for redistribution with larger packages where only HTTP GET and
    POST functionality are necessary.

    HTTP::Lite supports basic POST and GET operations only.  As of
    0.2.1, HTTP::Lite supports HTTP/1.1 and is compliant with the Host
    header, necessary for name based virtual hosting.  Additionally,
    HTTP::Lite now supports Proxies.

    As of 2.0.0 HTTP::Lite now supports a callback to allow processing
    of request data as it arrives.  This is useful for handling very
    large files without consuming memory.

    If you require more functionality, such as FTP or HTTPS, please
    see libwwwperl (LWP).  LWP is a significantly better and more
    comprehensive package than HTTP::Lite, and should be used instead
    of HTTP::Lite whenever possible.

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

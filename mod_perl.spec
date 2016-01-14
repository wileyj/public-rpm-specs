%define         _version 2.0.7
%define         _release 1.%{dist}
%define         _source http://perl.apache.org/dist/mod_perl-2.0.7.tar.gz
%define         _httpd_min_ver 2.2.0
%define         _perl_min_ver 5.6.1
%define		_apache_dir /opt/apache2.2
Name:           mod_perl
Version:        %{_version}
Release:        %{_release}
Summary:        An embedded Perl interpreter for the Apache Web server
Group:          System Environment/Daemons
License:        Apache License, Version 2.0
Vendor: %{vendor}
Packager: %{packager}
URL:            http://perl.apache.org/
Source0:         %{_source}
Source1:        filter-requires.sh
Source2:        filter-provides.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       httpd >= %{_httpd_min_ver}
%if 0%{?el6}
BuildRequires:  httpd-devel apr-devel apr-util-devel e2fsprogs-devel perl-Data-Flow cyrus-sasl-devel  gdbm-devel
BuildRequires:  expat-devel libcom_err-devel openldap-devel  httpd httpd-tools perl-Test-Harness
BuildRequires:  perl perl-ExtUtils-CBuilder, perl-ExtUtils-MakeMaker, perl-devel, perl-libs, perl-ExtUtils-Embed
%else
BuildRequires:  perl >= %{_perl_min_ver}
BuildRequires:  httpd >= %{_httpd_min_ver}, httpd-devel
BuildRequires:  apr-devel, apr-util-devel , e2fsprogs-devel
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Data::Flow)
BuildRequires:  gdbm-devel
%endif

%define __perl_requires %{SOURCE1}
%define __perl_provides %{SOURCE2}

%description
Mod_perl incorporates a Perl interpreter into the Apache web server,
so that the Apache web server can directly execute Perl code.
Mod_perl links the Perl runtime library into the Apache web server and
provides an object-oriented Perl interface for Apache's C language
API.  The end result is a quicker CGI script turnaround process, since
no external Perl interpreter has to be started.

Install mod_perl if you're installing the Apache web server and you'd
like for it to directly incorporate a Perl interpreter.

%package devel
Summary:        Files needed for building XS modules that use mod_perl
Group:          Development/Libraries
Requires:       mod_perl = %{version}-%{release}, httpd-devel

%description devel 
The mod_perl-devel package contains the files needed for building XS
modules that use mod_perl.

%prep
%setup -q 
if [ ! -f "/usr/lib64/libperl.so" ]
then
	ln -s /usr/lib64/perl5/CORE/libperl.so /usr/lib64/libperl.so
fi
%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL </dev/null \
	PREFIX=$RPM_BUILD_ROOT/usr \
	INSTALLDIRS=vendor \
	MP_APXS=%{_apache_dir}/bin/apxs
        MP_APR_CONFIG=%{_apache_dir}/bin/apr-1-config

make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_apache_dir}/modules
make install \
    MODPERL_AP_LIBEXECDIR=$RPM_BUILD_ROOT%{_apache_dir}/modules \
    MODPERL_AP_INCLUDEDIR=$RPM_BUILD_ROOT%{_apache_dir}/include

# Remove the temporary files.
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'


# Fix permissions to avoid strip failures on non-root builds.
chmod -R u+w $RPM_BUILD_ROOT/*

# Move set of modules to -devel
devmods="ModPerl::Code ModPerl::BuildMM ModPerl::CScan \
          ModPerl::TestRun ModPerl::Config ModPerl::WrapXS \
          ModPerl::BuildOptions ModPerl::Manifest \
          ModPerl::MapUtil ModPerl::StructureMap \
          ModPerl::TypeMap ModPerl::FunctionMap \
          ModPerl::ParseSource ModPerl::MM \
          Apache2::Build Apache2::ParseSource Apache2::BuildConfig \
          Bundle::ApacheTest"

for m in $devmods; do
   test -f $RPM_BUILD_ROOT%{_mandir}/man3/${m}.3pm &&
     echo "%{_mandir}/man3/${m}.3pm*"
   fn=${m//::/\/}
   test -f $RPM_BUILD_ROOT%{perl_vendorarch}/${fn}.pm &&
        echo %{perl_vendorarch}/${fn}.pm
   test -d $RPM_BUILD_ROOT%{perl_vendorarch}/${fn} && 
        echo %{perl_vendorarch}/${fn}
   test -d $RPM_BUILD_ROOT%{perl_vendorarch}/auto/${fn} && 
        echo %{perl_vendorarch}/auto/${fn}
done | tee devel.files | sed 's/^/%%exclude /' > exclude.files

echo "%%exclude %{_mandir}/man3/Apache::Test*.3pm*" >> exclude.files

# perl build script generates *.orig files, they get installed and later they
# break provides so mod_perl requires mod_perl-devel. We remove them here.
find "$RPM_BUILD_ROOT" -type f -name *.orig -exec rm -f {} \;

cat exclude.files > %{name}-%{version}-%{release}-filelist
find $RPM_BUILD_ROOT -type f | sed s/3pm/3pm.gz/g | sed "s@^$RPM_BUILD_ROOT@@g" >> %{name}-%{version}-%{release}-filelist
sed 's/3pm*/3pm.gz/g' devel.files | sed 's/*//g' | sed 's/[]\/()$*.^|[]/\\&/g'  > escape.files
for i in `cat escape.files`; do
  sed -i -e 's/'${i}'//g' %{name}-%{version}-%{release}-filelist 
done

if [ "$(cat %{name}-%{version}-%{release}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi
sed -i -e 's/\/autosplit.ix/\/usr\/lib64\/perl5\/vendor_perl\/auto\/Apache2\/Build\/autosplit.ix/g' %{name}-%{version}-%{release}-filelist

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files -f  %{name}-%{version}-%{release}-filelist
%defattr(-,root,root,-)

%files devel -f devel.files
%defattr(-,root,root,-)
%{_apache_dir}/include/*
#%{perl_vendorarch}/Apache/Test*.pm
#%{perl_vendorarch}/MyTest
%{_mandir}/man3/Apache::Test*.3pm*
%changelog

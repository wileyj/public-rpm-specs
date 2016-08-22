%define macro %{_rpmconfigdir}/macros.d/macros.python
%include %{macro}

%define vimdir %(ls -d %{_datadir}/vim/{vimfiles,vim[0-9]*} 2>/dev/null | tail -1)
Summary: Tool to convert AsciiDoc text files to DocBook, HTML or Unix man pages
Name: asciidoc
Version: 8.6.9
Release: 1.%{?dist}
License: GPL
Group: Applications/Text
URL: http://www.methods.co.nz/asciidoc/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/asciidoc/asciidoc-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: python27-devel, python-srpm-macros
BuildRequires: git python-srpm-macros
Requires: docbook-style-xsl
Requires: libxslt
%description
AsciiDoc is a text document format for writing short documents, articles,
books and UNIX man pages. AsciiDoc files can be translated to HTML and
DocBook markups using the asciidoc(1) command.

%prep
%setup

### Fix dependency on Docbook v4.5 for other distributions
%{?docbook_version:%{__perl} -pi.orig -e 's|4\.5\b|%{docbook_version}|g' docbook.conf}

%build
%configure

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

### rest to datadir; symlinks so asciidoc works
%{__mkdir} -p %{buildroot}%{_datadir}/asciidoc/
for dir in docbook-xsl/ images/ javascripts/ stylesheets/; do
    %{__mv} -v %{buildroot}%{_sysconfdir}/asciidoc/$dir %{buildroot}%{_datadir}/asciidoc/
    %{__ln_s} -vf %{_datadir}/asciidoc/$dir %{buildroot}%{_sysconfdir}/asciidoc/
done

### Python API
%{__install} -Dp -m0644 asciidocapi.py %{buildroot}%{python_sitelib}/asciidocapi.py

### Make it easier to %exclude these with both rpm < and >= 4.7
for file in %{buildroot}{%{_bindir},%{_sysconfdir}/asciidoc/filters/*}/*.py ; do
    touch ${file}{c,o}
done

for file in $(cd vim; find * -type f); do
    %{__install} -Dp -m0644 vim/$file %{buildroot}%{vimdir}/$file
done

#%{__install} -Dp -m0755 asciidoc.py %{buildroot}%{_bindir}/asciidoc
#%{__install} -Dp -m0755 a2x %{buildroot}%{_bindir}/a2x
#%{__install} -Dp -m0644 doc/asciidoc.1 %{buildroot}%{_mandir}/man1/asciidoc.1
#%{__install} -Dp -m0644 doc/a2x.1 %{buildroot}%{_mandir}/man1/a2x.1

#%{__install} -d -m0755 %{buildroot}%{_datadir}/asciidoc/
#%{__cp} -pR docbook-xsl/ images/ javascripts/ stylesheets/ %{buildroot}%{_datadir}/asciidoc/

#%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/asciidoc/
#%{__install} -p -m0644 *.conf %{buildroot}%{_sysconfdir}/asciidoc/
#%{__cp} -pR filters/ %{buildroot}%{_sysconfdir}/asciidoc/
#%{__ln_s} -f %{_datadir}/asciidoc/docbook-xsl/ %{buildroot}%{_sysconfdir}/asciidoc/
#%{__ln_s} -f %{_datadir}/asciidoc/images/ %{buildroot}%{_sysconfdir}/asciidoc/
#%{__ln_s} -f %{_datadir}/asciidoc/javascripts/ %{buildroot}%{_sysconfdir}/asciidoc/
#%{__ln_s} -f %{_datadir}/asciidoc/stylesheets/ %{buildroot}%{_sysconfdir}/asciidoc/

### Fix symlinks in examples/
#%{__install} -d -m0755 symlinks/
#%{__ln_s} -f %{_sysconfdir}/asciidoc/filters/ symlinks/filters
#%{__ln_s} -f %{_sysconfdir}/asciidoc/images/ symlinks/images
#%{__ln_s} -f %{_sysconfdir}/asciidoc/javascripts/ symlinks/javascripts
#%{__ln_s} -f %{_sysconfdir}/asciidoc/stylesheets/ symlinks/stylesheets

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root, 0755)
%doc BUGS* CHANGELOG* COPYING COPYRIGHT INSTALL* README*
%doc doc/ examples/ vim/
%doc %{_mandir}/man1/a2x.1*
%doc %{_mandir}/man1/asciidoc.1*
%config(noreplace) %{_sysconfdir}/asciidoc/
%{_bindir}/a2x
%{_bindir}/a2x.py
%{_bindir}/asciidoc
%{_bindir}/asciidoc.py
%{_datadir}/asciidoc/
%{python_sitelib}/asciidocapi.py*
%dir %{vimdir}
#%dir %{vimdir}/ftdetect/
#%{vimdir}/ftdetect/asciidoc_filetype.vim
%dir %{vimdir}/syntax/
%{vimdir}/syntax/asciidoc.vim
%exclude %{_bindir}/*.py[co]
%exclude %{_sysconfdir}/asciidoc/filters/*/*.py[co]

%changelog

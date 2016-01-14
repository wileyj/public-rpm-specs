%define cpan_name XML::DOM
%define pkgname XML-DOM
%define cpan_version %(echo `curl -s https://metacpan.org/pod/%{cpan_name} | grep "Module version" | cut -d":" -f2`)
%define filelist %{pkgname}-%{version}-filelist

name:      perl-XML-DOM
summary:   XML-DOM - A perl module for building DOM Level 1 compliant document structures
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
%if 0%{?el6}
buildarch: x86_64
%else
buildarch: noarch
%endif
Provides: %{name}
%{?load: %{_sourcedir}/macros.perl}

%description
This module extends the XML::Parser module by Clark Cooper. 
The XML::Parser module is built on top of XML::Parser::Expat, 
which is a lower level interface to James Clark's expat library.

XML::DOM::Parser is derived from XML::Parser. It parses XML strings or files
and builds a data structure that conforms to the API of the Document Object 
Model as described at http://www.w3.org/TR/REC-DOM-Level-1.
See the XML::Parser manpage for other available features of the 
XML::DOM::Parser class. 
Note that the 'Style' property should not be used (it is set internally.)

The XML::Parser *NoExpand* option is more or less supported, in that it will
generate EntityReference objects whenever an entity reference is encountered
in character data. I'm not sure how useful this is. Any comments are welcome.

As described in the synopsis, when you create an XML::DOM::Parser object, 
the parse and parsefile methods create an *XML::DOM::Document* object
from the specified input. This Document object can then be examined, modified and
written back out to a file or converted to a string.

When using XML::DOM with XML::Parser version 2.19 and up, setting the 
XML::DOM::Parser option *KeepCDATA* to 1 will store CDATASections in
CDATASection nodes, instead of converting them to Text nodes.
Subsequent CDATASection nodes will be merged into one. Let me know if this
is a problem.

When using XML::Parser 2.27 and above, you can suppress expansion of
parameter entity references (e.g. %pent;) in the DTD, by setting *ParseParamEnt*
to 1 and *ExpandParamEnt* to 0. See Hidden Nodes for details.

A Document has a tree structure consisting of *Node* objects. A Node may contain
other nodes, depending on its type.
A Document may have Element, Text, Comment, and CDATASection nodes. 
Element nodes may have Attr, Element, Text, Comment, and CDATASection nodes. 
The other nodes may not have any child nodes. 

This module adds several node types that are not part of the DOM spec (yet.)
These are: ElementDecl (for <!ELEMENT ...> declarations), AttlistDecl (for
<!ATTLIST ...> declarations), XMLDecl (for <?xml ...?> declarations) and AttDef
(for attribute definitions in an AttlistDecl.)

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
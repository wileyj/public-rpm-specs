%global gem_name rmagick
%define repo https://rubygems.org/api/v1/gems
%global gem_version %(echo `curl -s %{repo}/%{gem_name}.json | jq '.version' | tr -d '"'`)
%global gem_summary %( echo ` curl -s %{repo}/%{gem_name}.json | jq '.info' | sed -e 's/\\n/ /g' | tr -d '"'`)
%define MVERSION 7.0.4
%define MPATCH 4
%define _imagemagick /opt/ImageMagick-%{MVERSION}

Name: rubygem-%{gem_name}
Version: %{gem_version}
Release: 1.%{dist}
Summary: %{gem_summary}
Group: Development/Languages
License: Ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems 
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby ruby-devel
BuildRequires:	rubygem-rpm-macros
BuildRequires:	ruby-rpm-macros ImageMagick-devel = %{MVERSION}.%{MPATCH}

Provides: rubygem-%{gem_name} = %{version}
Provides: rubygem(%{gem_name}) = %{version}
Obsoletes: rubygem-%{gem_name} < %{version}
Obsoletes: rubygem(%{gem_name}) < %{version}

%description
%{summary}

%prep
export PATH=$PATH:$JAVA_HOME/bin:%{_imagemagick}/bin
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{pkgconfig}
export CPPFLAGS="-I%{_imagemagick}/include"
export LDFLAGS="-L%{_imagemagick}/lib"
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{_builddir}/%{name}/%{gem_dir} --bindir %{_builddir}/%{name}/%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gem_name}

%build

%install
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;
cp -pa %{_builddir}/%{name}/* %{buildroot}/

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files 
%{gem_dir}/*

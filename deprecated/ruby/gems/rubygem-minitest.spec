%global gem_name minitest
%define repo https://rubygems.org/api/v1/gems
%global gem_version %(echo `curl -s %{repo}/%{gem_name}.json | jq '.version' | tr -d '"'`)
#%global gem_summary %( echo ` curl -s %{repo}/%{gem_name}.json | jq '.info' | sed -e 's/\\n/ /g' | tr -d '"'`)
%global gem_summary 'rubygeem %{gem_name}'

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
##BuildRequires:  rubygem-rpm-macros
##BuildRequires:  ruby-rpm-macros
Provides: rubygem-%{gem_name}
Provides: rubygem(%{gem_name})
Obsoletes: rubygem-%{gem_name} < %{version}
Obsoletes: rubygem(%{gem_name}) < %{version}
Requires: rubygem-i18n
Requires: rubygem-json
Requires: rubygem-tzinfo
Requires: rubygem-minitest
Requires: rubygem-thread_safe

%description
%{summary}

%prep
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{_builddir}/%{name}/%{gem_dir} --bindir %{_builddir}/%{name}/%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gem_name}

%build

%install
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;
cp -pa %{_builddir}/%{name}/* %{buildroot}/

if [ -f %{buildroot}%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
    sed -i -e 's|", "[0-9].*|"|g' %{buildroot}%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
fi
if [ -f %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec
    sed -i -e 's|", "[0-9].*|"|g'  %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec
fi

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files 
%{gem_dir}/*

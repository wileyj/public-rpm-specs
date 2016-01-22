# Generated from sensu-plugins-sensu-plugins-consul-0.0.1.gem by gem2rpm -*- rpm-spec -*-
# This is template file fedora.spec.rb: /usr/share/gems/gems/gem2rpm-<version>/templates/fedora.spec.erb
#AutoReqProv: no


%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global gemname sensu-plugins-sensu-plugins-consul

%global geminstdir %{gem_dir}/gems/%{gemname}-%{version}
%global rubyabi 2.1.0

Summary: Sensu plugins for working with Consul
Name: rubygem-%{gemname}
Version: 0.0.1
Release: 1.%{dist}
Group: Development/Languages
License: Ruby
Vendor: %{vendor}
Packager: %{packager}
Source0: %{gemname}-%{version}.gem
Requires: ruby rubygems
Requires: rubygem-sensu-plugin
Requires: rubygem-rest-client
Requires: rubygem-diplomat
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby
BuildArch: x86_64
Provides: rubygem-%{gemname}

%description
Sensu plugins for working with Consul.




%prep
%setup -q -c -T
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0} \
	    --no-rdoc --no-ri --no-doc

%build

%install
find %{_builddir}/%{name}-%{version} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \; 
cp -pa ./* %{buildroot}/


if [ -f %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec ]
then
	sed -e '/s.installed_by_version/ s/^#*/#/' -i  %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec
fi

(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    if [ -d %{buildroot}%{gem_dir}/cache ]
    then
        echo '%exclude "%{gem_dir}/cache"'
    fi
    if [ -f %{buildroot}%{gem_dir}/cache/%{gemname}-%{version}.gem ]
    then
        echo '%exclude "%{gem_dir}/cache/%{gemname}-%{version}.gem"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/.gitignore ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-%{version}/.gitignore"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/.travis.yml ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-%{version}/.travis.yml"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/.yardopts ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-%{version}/.yardopts"'
    fi
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache/%{gemname}-%{version}.gem'
) > filelist
%{__sed} -i -e 's/%dir ""//g' filelist

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files -f filelist

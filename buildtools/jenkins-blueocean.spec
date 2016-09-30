%define repo https://github.com/jenkinsci/blueocean-plugin
%define _prefix	/opt/%{name}
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1 | cut -c1-7`)
%define rel_version 1

Name:		jenkins-blueocean
Version:	162
Release:	%{rel_version}.%{revision}.%{dist}
Summary:	Continous Build Server UI
URL:		http://jenkins-ci.org/
Group:		Development/Tools/Building
License:	MIT/X License, GPL/CDDL, ASL2
Vendor: 	%{vendor}
Packager: 	%{packager}
BuildRoot:	%{_tmppath}/build-%{name}-%{version}
BuildRequires:	maven nodejs
Requires: jenkins
Requires:	maven nodejs
Requires: %{name}-bin
Requires: %{name}-commons
Requires: %{name}-config
Requires: %{name}-core-js
Requires: %{name}-dashboard
Requires: %{name}-events
Requires: %{name}-personalization
Requires: %{name}-pipeline-api-impl
Requires: %{name}-rest
Requires: %{name}-web
Requires: %{name}-docker

BuildArch:	x86_64

%description
Blue Ocean is the next generation user experience for Jenkins.
It is a multi-module maven project with a few Jenkins plugins.

%package -n %{name}-bin
Group: Development/Tools/Building
Summary:	Continous Build Server UI bin files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-bin
Continous Build Server UI bin files

%package -n %{name}-commons
Group: Development/Tools/Building
Summary:	Continous Build Server UI commons files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-commons
Continous Build Server UI commons files

%package -n %{name}-config
Group: Development/Tools/Building
Summary:	Continous Build Server UI config files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-config
Continous Build Server UI config files

%package -n %{name}-js
Group: Development/Tools/Building
Summary:	Continous Build Server UI js files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-js
Continous Build Server UI js files

%package -n %{name}-dashboard
Group: Development/Tools/Building
Summary:	Continous Build Server UI dashboard files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-dashboard
Continous Build Server UI dashboard files

%package -n %{name}-events
Group: Development/Tools/Building
Summary:	Continous Build Server UI events files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-events
Continous Build Server UI events files

%package -n %{name}-jwt
Group: Development/Tools/Building
Summary:	Continous Build Server UI jwt files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-jwt
Continous Build Server UI jwt files

%package -n %{name}-personalization
Group: Development/Tools/Building
Summary:	Continous Build Server UI personalization files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-personalization
Continous Build Server UI personalization files

%package -n %{name}-pipeline-api-impl
Group: Development/Tools/Building
Summary:	Continous Build Server UI pipeline-api-impl files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-pipeline-api-impl
Continous Build Server UI pipeline-api-impl files

%package -n %{name}-rest
Group: Development/Tools/Building
Summary:	Continous Build Server UI rest files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-rest
Continous Build Server UI rest files

%package -n %{name}-web
Group: Development/Tools/Building
Summary:	Continous Build Server UI web files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-web
Continous Build Server UI web files

%package -n %{name}-docker
Group: Development/Tools/Building
Summary:	Continous Build Server UI docker files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-docker
Continous Build Server UI docker files



%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
mvn clean install -DskipTests

%install
cd %{name}-%{version}
rm -rf %{buildroot}

%__install -d %{buildroot}%{_prefix}
%__install -d %{buildroot}%{_prefix}/bin
%__install -d %{buildroot}%{_prefix}/blueocean
%__install -d %{buildroot}%{_prefix}/blueocean-commons
%__install -d %{buildroot}%{_prefix}/blueocean-config/etc
%__install -d %{buildroot}%{_prefix}/blueocean-core-js
%__install -d %{buildroot}%{_prefix}/blueocean-dashboard
%__install -d %{buildroot}%{_prefix}/blueocean-events
%__install -d %{buildroot}%{_prefix}/blueocean-jwt
%__install -d %{buildroot}%{_prefix}/blueocean-personalization
%__install -d %{buildroot}%{_prefix}/blueocean-pipeline-api-impl
%__install -d %{buildroot}%{_prefix}/blueocean-rest
%__install -d %{buildroot}%{_prefix}/blueocean-rest-impl
%__install -d %{buildroot}%{_prefix}/blueocean-web
%__install -d %{buildroot}%{_prefix}/blueocean-web/etc

cp -pa docker %{buildroot}%{_prefix}/docker
cp -pa docker-demo %{buildroot}%{_prefix}/docker-demo
cp -pa js-extensions %{buildroot}%{_prefix}/js-extensions
cp -pa licenses /%{buildroot}%{_prefix}/licenses
cp -pa target/blueocean-parent/WEB-INF %{buildroot}%{_prefix}/WEB-INF
cp -pa bin/* %{buildroot}%{_prefix}/bin/

%__install -m0644 CONTRIBUTING.md %{buildroot}%{_prefix}/CONTRIBUTING.md
%__install -m0644 Dockerfile %{buildroot}%{_prefix}/Dockerfile
%__install -m0644 Jenkinsfile %{buildroot}%{_prefix}/Jenkinsfile
%__install -m0644 LICENSE.txt %{buildroot}%{_prefix}/LICENSE.txt
%__install -m0644 logo-yarrr.png %{buildroot}%{_prefix}/logo-yarrr.png 
%__install -m0644 pom.xml %{buildroot}%{_prefix}/pom.xml
%__install -m0644 PULL_REQUEST_TEMPLATE %{buildroot}%{_prefix}/PULL_REQUEST_TEMPLATE
%__install -m0644 README.md %{buildroot}%{_prefix}/README.md

cp -pa blueocean/target/*.jar %{buildroot}%{_prefix}/blueocean/
cp -pa blueocean/target/*.hpi %{buildroot}%{_prefix}/blueocean/
cp -pa blueocean/work %{buildroot}%{_prefix}/blueocean/
cp -pa blueocean-commons/target/*.jar %{buildroot}%{_prefix}/blueocean-commons/
cp -pa blueocean-commons/target/*.hpi %{buildroot}%{_prefix}/blueocean-commons/
cp -pa blueocean-config/target/*.jar %{buildroot}%{_prefix}/blueocean-config/
cp -pa blueocean-config/target/*.hpi %{buildroot}%{_prefix}/blueocean-config/
cp -pa blueocean-config/etc %{buildroot}%{_prefix}/blueocean-config/
cp -pa blueocean-core-js/target/*.jar %{buildroot}%{_prefix}/blueocean-core-js/
cp -pa blueocean-core-js/target/*.hpi %{buildroot}%{_prefix}/blueocean-core-js/
cp -pa blueocean-dashboard/target/*.jar %{buildroot}%{_prefix}/blueocean-dashboard/
cp -pa blueocean-dashboard/target/*.hpi %{buildroot}%{_prefix}/blueocean-dashboard/
cp -pa blueocean-events/target/*.jar %{buildroot}%{_prefix}/blueocean-events/
cp -pa blueocean-events/target/*.hpi %{buildroot}%{_prefix}/blueocean-events/
cp -pa blueocean-jwt/target/*.jar %{buildroot}%{_prefix}/blueocean-jwt/
cp -pa blueocean-jwt/target/*.hpi %{buildroot}%{_prefix}/blueocean-jwt/
cp -pa blueocean-personalization/target/* %{buildroot}%{_prefix}/blueocean-personalization/
cp -pa blueocean-pipeline-api-impl/target/*.jar %{buildroot}%{_prefix}/blueocean-pipeline-api-impl/
cp -pa blueocean-pipeline-api-impl/target/*.hpi %{buildroot}%{_prefix}/blueocean-pipeline-api-impl/
cp -pa blueocean-rest/target/*.jar %{buildroot}%{_prefix}/blueocean-rest/
cp -pa blueocean-rest/target/*.hpi %{buildroot}%{_prefix}/blueocean-rest/
cp -pa blueocean-rest-impl/target/*.jar %{buildroot}%{_prefix}/blueocean-rest-impl/
cp -pa blueocean-rest-impl/target/*.hpi %{buildroot}%{_prefix}/blueocean-rest-impl/
cp -pa blueocean-web/target/*.jar %{buildroot}%{_prefix}/blueocean-web/
cp -pa blueocean-web/target/*.hpi %{buildroot}%{_prefix}/blueocean-web/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%dir %{_prefix}/blueocean
%dir %{_prefix}/licenses
%dir %{_prefix}/target
%dir %{_prefix}/blueocean
%dir %{_prefix}/WEB-INF
%config(noreplace)  %{_prefix}/Jenkinsfile
%config(noreplace)  %{_prefix}/pom.xml
%config(noreplace)  %{_prefix}/Dockerfile
%{_prefix}/PULL_REQUEST_TEMPLATE 
%{_prefix}/README.md 
%{_prefix}/CONTRIBUTING.md 
%{_prefix}/LICENSE.txt
%{_prefix}/licenses/*
%{_prefix}/logo-yarrr.png
%{_prefix}/WEB-INF/*
%{_prefix}/blueocean/*


%files -n %{name}-bin
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/bin
%attr(0755,root,root) %{_prefix}/bin/build-in-docker.sh  
%attr(0755,root,root) %{_prefix}/bin/checkdeps.js  
%attr(0755,root,root) %{_prefix}/bin/checkshrinkwrap.js  
%attr(0755,root,root) %{_prefix}/bin/cleanInstall.js  
%attr(0755,root,root) %{_prefix}/bin/git-helper.sh  
%attr(0755,root,root) %{_prefix}/bin/jwtcurl.sh  
%attr(0755,root,root) %{_prefix}/bin/setup.sh  
%attr(0755,root,root) %{_prefix}/bin/start.sh
%attr(0644,root,root) %{_prefix}/bin/package.json  

%files -n %{name}-commons
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-commons
%{_prefix}/blueocean-commons/*


%files -n %{name}-config
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-config
%{_prefix}/blueocean-config/*

%files -n %{name}-js
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-core-js
%{_prefix}/blueocean-core-js/*

%files -n %{name}-dashboard
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-dashboard
%{_prefix}/blueocean-dashboard/*

%files -n %{name}-events
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-events
%{_prefix}/blueocean-events/*

%files -n %{name}-jwt
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-jwt
%{_prefix}/blueocean-jwt/*

%files -n %{name}-personalization
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-personalization
%{_prefix}/blueocean-personalization/*

%files -n %{name}-pipeline-api-impl
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-pipeline-api-impl
%{_prefix}/blueocean-pipeline-api-impl/*

%files -n %{name}-rest
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-rest
%dir %{_prefix}/blueocean-rest-impl
%{_prefix}/blueocean-rest/*
%{_prefix}/blueocean-rest-impl/*

%files -n %{name}-web
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/blueocean-web
%{_prefix}/blueocean-web/*

%files -n %{name}-docker
%defattr(-,jenkins,jenkins)
%dir %{_prefix}/docker
%dir %{_prefix}/docker-demo
%{_prefix}/docker/*
%{_prefix}/docker-demo/*


%changelog


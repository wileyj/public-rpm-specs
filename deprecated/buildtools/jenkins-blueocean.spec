%define repo https://github.com/jenkinsci/blueocean-plugin
%define jb_prefix	/opt/%{name}
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d 'blueocean-parent\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1 | cut -c1-7`)
%define rel_version 1

Name:		jenkins-blueocean
Version:	%{gitversion}
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

%package -n %{name}-core-js
Group: Development/Tools/Building
Summary:	Continous Build Server UI js files
Requires: %{name} = %{version}-%{release}

%description -n %{name}-core-js
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
/opt/maven/bin/mvn clean install -DskipTests

%install
cd %{name}-%{version}
rm -rf %{buildroot}

%__install -d %{buildroot}%{jb_prefix}
%__install -d %{buildroot}%{jb_prefix}/bin
%__install -d %{buildroot}%{jb_prefix}/blueocean
%__install -d %{buildroot}%{jb_prefix}/blueocean-commons
%__install -d %{buildroot}%{jb_prefix}/blueocean-config/etc
%__install -d %{buildroot}%{jb_prefix}/blueocean-core-js
%__install -d %{buildroot}%{jb_prefix}/blueocean-dashboard
%__install -d %{buildroot}%{jb_prefix}/blueocean-events
%__install -d %{buildroot}%{jb_prefix}/blueocean-jwt
%__install -d %{buildroot}%{jb_prefix}/blueocean-personalization
%__install -d %{buildroot}%{jb_prefix}/blueocean-pipeline-api-impl
%__install -d %{buildroot}%{jb_prefix}/blueocean-rest
%__install -d %{buildroot}%{jb_prefix}/blueocean-rest-impl
%__install -d %{buildroot}%{jb_prefix}/blueocean-web
%__install -d %{buildroot}%{jb_prefix}/blueocean-web/etc

cp -pa docker %{buildroot}%{jb_prefix}/docker
cp -pa docker-demo %{buildroot}%{jb_prefix}/docker-demo
cp -pa js-extensions %{buildroot}%{jb_prefix}/js-extensions
cp -pa licenses /%{buildroot}%{jb_prefix}/licenses
cp -pa target/blueocean-parent/WEB-INF %{buildroot}%{jb_prefix}/WEB-INF
cp -pa bin/* %{buildroot}%{jb_prefix}/bin/

%__install -m0644 CONTRIBUTING.md %{buildroot}%{jb_prefix}/CONTRIBUTING.md
%__install -m0644 Dockerfile %{buildroot}%{jb_prefix}/Dockerfile
%__install -m0644 Jenkinsfile %{buildroot}%{jb_prefix}/Jenkinsfile
%__install -m0644 LICENSE.txt %{buildroot}%{jb_prefix}/LICENSE.txt
%__install -m0644 docu/pix/logo-yarrr.png %{buildroot}%{jb_prefix}/logo-yarrr.png 
%__install -m0644 pom.xml %{buildroot}%{jb_prefix}/pom.xml
%__install -m0644 PULL_REQUEST_TEMPLATE %{buildroot}%{jb_prefix}/PULL_REQUEST_TEMPLATE
%__install -m0644 README.md %{buildroot}%{jb_prefix}/README.md

cp -pa blueocean/target/*.jar %{buildroot}%{jb_prefix}/blueocean/
cp -pa blueocean/target/*.hpi %{buildroot}%{jb_prefix}/blueocean/
cp -pa blueocean/target/plugins %{buildroot}%{jb_prefix}/blueocean/
cp -pa blueocean/target/blueocean %{buildroot}%{jb_prefix}/blueocean/
cp -pa blueocean/work %{buildroot}%{jb_prefix}/blueocean/

cp -pa blueocean-commons/target/*.jar %{buildroot}%{jb_prefix}/blueocean-commons/
cp -pa blueocean-commons/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-commons/
cp -pa blueocean-commons/target/blueocean-commons %{buildroot}%{jb_prefix}/blueocean-commons/

cp -pa blueocean-config/target/*.jar %{buildroot}%{jb_prefix}/blueocean-config/
cp -pa blueocean-config/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-config/
cp -pa blueocean-config/target/blueocean-config %{buildroot}%{jb_prefix}/blueocean-config/
cp -pa blueocean-config/etc %{buildroot}%{jb_prefix}/blueocean-config/

cp -pa blueocean-core-js/* %{buildroot}%{jb_prefix}/blueocean-core-js/

cp -pa blueocean-dashboard/etc %{buildroot}%{jb_prefix}/blueocean-dashboard/
cp -pa blueocean-dashboard/target/*.jar %{buildroot}%{jb_prefix}/blueocean-dashboard/
cp -pa blueocean-dashboard/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-dashboard/
cp -pa blueocean-dashboard/target/blueocean-dashboard %{buildroot}%{jb_prefix}/blueocean-dashboard/

cp -pa blueocean-events/target/*.jar %{buildroot}%{jb_prefix}/blueocean-events/
cp -pa blueocean-events/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-events/
cp -pa blueocean-events/target/blueocean-events %{buildroot}%{jb_prefix}/blueocean-events/

cp -pa blueocean-jwt/target/*.jar %{buildroot}%{jb_prefix}/blueocean-jwt/
cp -pa blueocean-jwt/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-jwt/
cp -pa blueocean-jwt/target/blueocean-jwt %{buildroot}%{jb_prefix}/blueocean-jwt/

cp -pa blueocean-personalization/target/*.jar %{buildroot}%{jb_prefix}/blueocean-personalization/
cp -pa blueocean-personalization/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-personalization/
cp -pa blueocean-personalization/target/blueocean-personalization %{buildroot}%{jb_prefix}/blueocean-personalization/
cp -pa blueocean-personalization/etc %{buildroot}%{jb_prefix}/blueocean-personalization/

cp -pa blueocean-pipeline-api-impl/target/*.jar %{buildroot}%{jb_prefix}/blueocean-pipeline-api-impl/
cp -pa blueocean-pipeline-api-impl/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-pipeline-api-impl/
cp -pa blueocean-pipeline-api-impl/target/blueocean-pipeline-api-impl %{buildroot}%{jb_prefix}/blueocean-pipeline-api-impl/

cp -pa blueocean-rest/target/*.jar %{buildroot}%{jb_prefix}/blueocean-rest/
cp -pa blueocean-rest/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-rest/
cp -pa blueocean-rest/target/blueocean-rest %{buildroot}%{jb_prefix}/blueocean-rest/

cp -pa blueocean-rest-impl/target/*.jar %{buildroot}%{jb_prefix}/blueocean-rest-impl/
cp -pa blueocean-rest-impl/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-rest-impl/
cp -pa blueocean-rest-impl/target/blueocean-rest-impl %{buildroot}%{jb_prefix}/blueocean-rest-impl/

cp -pa blueocean-web/etc %{buildroot}%{jb_prefix}/blueocean-web/
cp -pa blueocean-web/target/*.jar %{buildroot}%{jb_prefix}/blueocean-web/
cp -pa blueocean-web/target/*.hpi %{buildroot}%{jb_prefix}/blueocean-web/
cp -pa blueocean-web/target/blueocean-web %{buildroot}%{jb_prefix}/blueocean-web/
cp -pa blueocean-web/target/frontend %{buildroot}%{jb_prefix}/blueocean-web/

%__rm -f %{buildroot}%{jb_prefix}/js-extensions/.gitignore
%__rm -f %{buildroot}%{jb_prefix}/js-extensions/.npmignore

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%dir %{jb_prefix}/blueocean
%dir %{jb_prefix}/licenses
%dir %{jb_prefix}/blueocean
%dir %{jb_prefix}/WEB-INF
%config(noreplace)  %{jb_prefix}/Jenkinsfile
%config(noreplace)  %{jb_prefix}/pom.xml
%config(noreplace)  %{jb_prefix}/Dockerfile
%{jb_prefix}/PULL_REQUEST_TEMPLATE 
%{jb_prefix}/README.md 
%{jb_prefix}/CONTRIBUTING.md 
%{jb_prefix}/LICENSE.txt
%{jb_prefix}/licenses/*
%{jb_prefix}/logo-yarrr.png
%{jb_prefix}/WEB-INF/*
%{jb_prefix}/blueocean/*


%files -n %{name}-bin
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/bin
%attr(0755,root,root) %{jb_prefix}/bin/build-in-docker.sh  
%attr(0755,root,root) %{jb_prefix}/bin/checkdeps.js  
%attr(0755,root,root) %{jb_prefix}/bin/checkshrinkwrap.js  
%attr(0755,root,root) %{jb_prefix}/bin/cleanInstall.js  
%attr(0755,root,root) %{jb_prefix}/bin/git-helper.sh  
%attr(0755,root,root) %{jb_prefix}/bin/jwtcurl.sh  
%attr(0755,root,root) %{jb_prefix}/bin/setup.sh  
%attr(0755,root,root) %{jb_prefix}/bin/start.sh
%attr(0644,root,root) %{jb_prefix}/bin/package.json  
%attr(0755,root,root) %{jb_prefix}/bin/ncuUpdate

%files -n %{name}-commons
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-commons
%{jb_prefix}/blueocean-commons/*


%files -n %{name}-config
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-config
%{jb_prefix}/blueocean-config/*

%files -n %{name}-core-js
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-core-js
%dir %{jb_prefix}/js-extensions
%{jb_prefix}/blueocean-core-js/*
%{jb_prefix}/js-extensions/*

%files -n %{name}-dashboard
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-dashboard
%{jb_prefix}/blueocean-dashboard/*

%files -n %{name}-events
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-events
%{jb_prefix}/blueocean-events/*

%files -n %{name}-jwt
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-jwt
%{jb_prefix}/blueocean-jwt/*

%files -n %{name}-personalization
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-personalization
%{jb_prefix}/blueocean-personalization/*

%files -n %{name}-pipeline-api-impl
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-pipeline-api-impl
%{jb_prefix}/blueocean-pipeline-api-impl/*

%files -n %{name}-rest
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-rest
%dir %{jb_prefix}/blueocean-rest-impl
%{jb_prefix}/blueocean-rest/*
%{jb_prefix}/blueocean-rest-impl/*

%files -n %{name}-web
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/blueocean-web
%{jb_prefix}/blueocean-web/*

%files -n %{name}-docker
%defattr(-,jenkins,jenkins)
%dir %{jb_prefix}/docker
%dir %{jb_prefix}/docker-demo
%{jb_prefix}/docker/*
%{jb_prefix}/docker-demo/*


%changelog


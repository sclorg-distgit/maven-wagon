%global pkg_name maven-wagon
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global bname     wagon

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.4
Release:        3.15%{?dist}
Epoch:          0
Summary:        Tools to manage artifacts and deployment
License:        ASL 2.0
URL:            http://maven.apache.org/wagon
Source0:        http://repo1.maven.org/maven2/org/apache/maven/wagon/wagon/%{version}/wagon-%{version}-source-release.zip

Patch0:         0001-Port-to-jetty-9.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(com.jcraft:jsch)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-httpclient:commons-httpclient)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-io:commons-io)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-lang:commons-lang)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-logging:commons-logging)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-net:commons-net)
BuildRequires:  %{?scl_prefix_java_common}mvn(easymock:easymock)
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix_java_common}mvn(log4j:log4j)
BuildRequires:  %{?scl_prefix_java_common}mvn(nekohtml:nekohtml)
BuildRequires:  maven30-mvn(org.apache.httpcomponents:httpclient:4.2)
BuildRequires:  maven30-mvn(org.apache.httpcomponents:httpcore:4.2)
BuildRequires:  maven30-mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  maven30-mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  maven30-mvn(org.apache.maven.scm:maven-scm-api)
BuildRequires:  maven30-mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  maven30-mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  maven30-mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  maven30-mvn(org.codehaus.plexus:plexus-interactivity-api)
BuildRequires:  maven30-mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-client)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-security)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-server)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-util)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.jsoup:jsoup)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.slf4j:slf4j-api)
BuildRequires:  %{?scl_prefix_java_common}mvn(xerces:xercesImpl)


%description
Maven Wagon is a transport abstraction that is used in Maven's
artifact and repository handling code. Currently wagon has the
following providers:
* File
* HTTP
* FTP
* SSH/SCP
* WebDAV
* SCM (in progress)

%package provider-test
Summary:        provider-test module for %{pkg_name}

%description provider-test
provider-test module for %{pkg_name}.

%package provider-api
Summary:        provider-api module for %{pkg_name}

%description provider-api
provider-api module for %{pkg_name}.

%package providers
Summary:        providers module for %{pkg_name}

%description providers
providers module for %{pkg_name}

%package file
Summary:        file module for %{pkg_name}

%description file
file module for %{pkg_name}.

%package ftp
Summary:        ftp module for %{pkg_name}

%description ftp
ftp module for %{pkg_name}.

%package http
Summary:        http module for %{pkg_name}

%description http
http module for %{pkg_name}.

%package http-shared
Summary:        http-shared module for %{pkg_name}

%description http-shared
http-shared module for %{pkg_name}.

%package http-shared4
Summary:        http-shared4 module for %{pkg_name}

%description http-shared4
http-shared4 module for %{pkg_name}.

%package http-lightweight
Summary:        http-lightweight module for %{pkg_name}

%description http-lightweight
http-lightweight module for %{pkg_name}.

%package scm
Summary:        scm module for %{pkg_name}

%description scm
scm module for %{pkg_name}.

%package ssh-external
Summary:        ssh-external module for %{pkg_name}

%description ssh-external
ssh-external module for %{pkg_name}.

%package ssh-common
Summary:        ssh-common module for %{pkg_name}

%description ssh-common
ssh-common module for %{pkg_name}.

%package ssh
Summary:        ssh module for %{pkg_name}

%description ssh
ssh module for %{pkg_name}.


%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n wagon-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x

%patch0 -p1

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_dep :wagon-tck-http wagon-providers/wagon-http

%pom_remove_dep :xercesMinimal wagon-providers/wagon-http-shared
%pom_xpath_inject "pom:dependencies" \
   "<dependency>
      <groupId>xerces</groupId>
      <artifactId>xercesImpl</artifactId>
    </dependency>" wagon-providers/wagon-http-shared

# correct groupId for jetty
%pom_xpath_replace "pom:groupId[text()='org.mortbay.jetty']" "<groupId>org.eclipse.jetty</groupId>"

# disable tests, missing dependencies
%pom_disable_module wagon-tcks
%pom_disable_module wagon-ssh-common-test wagon-providers/pom.xml

# missing dependencies
%pom_disable_module wagon-webdav-jackrabbit wagon-providers

%pom_change_dep -rf org.apache.httpcomponents:httpclient ::4.2
%pom_change_dep -rf org.apache.httpcomponents:httpcore ::4.2
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_file ":wagon-{*}" %{pkg_name}/@1

%mvn_package ":wagon"

# tests are disabled because of missing dependencies
%mvn_build -f -s

# Maven requires Wagon HTTP with classifier "shaded"
%mvn_alias :wagon-http :::shaded:
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE NOTICE DEPENDENCIES
%files provider-api -f .mfiles-wagon-provider-api
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files providers -f .mfiles-wagon-providers
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files file -f .mfiles-wagon-file
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files ftp -f .mfiles-wagon-ftp
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files http -f .mfiles-wagon-http
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files http-shared -f .mfiles-wagon-http-shared
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files http-shared4 -f .mfiles-wagon-http-shared4
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files http-lightweight -f .mfiles-wagon-http-lightweight
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files scm -f .mfiles-wagon-scm
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files ssh-external -f .mfiles-wagon-ssh-external
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files ssh-common -f .mfiles-wagon-ssh-common
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files ssh -f .mfiles-wagon-ssh
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%files provider-test -f .mfiles-wagon-provider-test
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE DEPENDENCIES

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 0:2.4-3.15
- maven33 rebuild

* Thu Jan 15 2015 Michael Simacek <msimacek@redhat.com> - 0:2.4-3.14
- Add common dirs to subpackages

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3.13
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michal Srb <msrb@redhat.com> - 2.4-3.12
- Build against httpcomponents 4.2 (compat)
- Fix BR

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:2.4-3.11
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:2.4-3.10
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3.9
- Mass rebuild 2014-05-26

* Wed Mar  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3.8
- Remove requires on parent POM

* Fri Feb 28 2014 Michael Simacek <msimacek@redhat.com> - 0:2.4-3.7
- Require main package

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 0:2.4-3.6
- Split into subpackages

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0:2.4-3.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 02.4-3
- Mass rebuild 2013-12-27

* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-2.2
- Add shaded alias for wagon-http

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Mar 01 2013 Michal Srb <msrb@redhat.com> - 0:2.4-1
- Port to jetty 9

* Thu Feb 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-1
- Simplify build-requires

* Thu Feb 14 2013 Michal Srb <msrb@redhat.com> - 0:2.4-1
- Update to latest upstream 2.4
- Remove old depmap and patches
- Build with xmvn

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-6
- Remove BR: ganymed-ssh2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-4
- Fix build against jetty 8 and servlet 3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Jaromir Capik <jcapik@redhat.com> - 0:1.0-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata

* Wed Jul 27 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-1
- Update to 1.0 final.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.22
- Install wagon-providers depmap too.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.21
- Install wagon pom depmap.
- Use maven 3 for build.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.b7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b7.1
- Update to beta 7.
- Adapt to current guidelines.
- Fix pom names.

* Thu Sep 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b6.3
- Use javadoc:aggregate.
- Drop ant build.
- Use global instead of define.

* Fri May 14 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.2
- Create patch for wagon-http-shared pom.xml

* Wed May 12 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.1
- Update to beta 6, build with with_maven 1

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.7
- Remove gcj parts.

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.6
- Update to beta2 - sync with jpackage.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.2.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  1 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0:1.0-0.1.a5.3.5
- include missing dir below _docdir

* Fri Oct 03 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3.4
- added patch to make it compatible with the newer version of jsch

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.1.a5.3.3
- drop repotag
- fix license tag

* Sat Apr 05 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.2
- Rebuild with new version of jsch

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.1
- Merge in the changes neeeded to build without jetty
- Fix rpmlint issues
- Generate new *-build.xml files from pom.xml files as origins of
  *-project files is unknown.
- Remove maven1 project.xml files from sources
- Comment out various section requiring maven or javadocs
  (to be re-enabled at a future time). Note that the ant:ant task
  for maven2 does not currently generate javadocs.

* Tue Apr 04 2006 Ralph Apel <r.apel@r-apel.de> - 0:1.0-0.a5.3jpp
- Require j-c-codec, to build with j-c-httpclient = 3.0

* Thu Dec 22 2005 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a5.2jpp
- Commented out potentially superfluous dependencies.
- Disabled wagon-scm

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a5.1jpp
- First JPackage build

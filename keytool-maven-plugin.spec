
%global group_id  org.codehaus.mojo

Name:             keytool-maven-plugin
Version:          1.0
Release:          5
Summary:          A plugin that wraps the keytool program and allows to manipulate keystores
License:          MIT and ASL 2.0
Group:            Development/Java
# http://mojo.codehaus.org/keytool-maven-plugin/
URL:              http://mojo.codehaus.org/%{name}/
# svn export http://svn.codehaus.org/mojo/tags/keytool-maven-plugin-1.0/ keytool-maven-plugin-1.0
# tar caf keytool-maven-plugin-1.0.tar.xz keytool-maven-plugin-1.0
Source0:          %{name}-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    maven

Requires:         java
Requires:         jpackage-utils
Requires:         maven
Requires:         plexus-utils
Requires:         apache-commons-lang

Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

%description
A plugin that wraps the keytool program bundled with Sun's Java SDK.
It provides the capability to manipulate keys and keystores
with the goals "keytool:genkey" and "keytool:clean".

%package javadoc
Summary:          API documentation for %{name}
Group:            Development/Java
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%build
mvn-rpmbuild install javadoc:aggregate

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap %{group_id} %{name} %{version} JPP %{name}

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc LICENSE.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt
%doc %{_javadocdir}/%{name}


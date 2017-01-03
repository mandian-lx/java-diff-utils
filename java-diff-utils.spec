%define commit 683d192aea15b8991d0a6d23567b064cb8496b62
%define shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:	A library for performing the comparison operations between texts 
Name:		java-diff-utils
Version:	1.4.0
Release:	1
License:	ASL 2.0
Group:		Development/Java
URL:		https://github.com/dnaumenko/%{name}
Source0:	https://github.com/dnaumenko/%{name}/archive/%{commit}/%{name}-%{commit}.zip
BuildArch:	noarch

BuildRequires:	java-rpmbuild
BuildRequires:	java-devel
BuildRequires:	maven-local
BuildRequires:	mvn(junit:junit)

%description
Diff Utils library is an OpenSource library for performing the comparison
operations between texts: computing diffs, applying patches, generating
unified diffs or parsing them, generating diff output for easy future
displaying (like side-by-side view) and so on.

Main reason to build this library was the lack of easy-to-use libraries
with all the usual stuff you need while working with diff files.

Originally it was inspired by JRCS library and it's nice design of diff
module.

This library implements Myer's diff algorithm. But it can easily replaced by
any other which is better for handing your texts. I have plan to add
implementation of some in future.

Main Features:

 *   computing the difference between two texts.
 *   capable to hand more than plain ascci. Arrays or List of any type that
	 implements hashCode() and equals() correctly can be subject to
	 differencing using this library
 *   patch and unpatch the text with the given patch
 *   parsing the unified diff format
 *   producing human-readable differences

%files -f .mfiles
%doc README.md
%doc LICENSE

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Requires:	jpackage-utils

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{commit}
# Delete all prebuild JARs
find . -name "*.jar" -delete
find . -name "*.class" -delete

# fix version
%pom_xpath_replace "pom:project/pom:version" "
	<version>%{version}</version>"

# ix jar-not-indexed warning
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]/pom:configuration/pom:archive" "
	<index>true</index>"

# Build a jar containing test-classes 
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]" "
<executions>
	<execution>
		<goals>
			<goal>test-jar</goal>
		</goals>
	</execution>
</executions>"

# Fix jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build

%install
%mvn_install


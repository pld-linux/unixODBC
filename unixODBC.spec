Summary:	unixODBC - a complete, free/open, ODBC solution for UNIX/Linux
Summary(pl):	unixODBC - kompletne, darmowe/otwarte ODBC dla UNIX/Linuksa
Name:		unixODBC
Version:	2.2.6
Release:	1.20030624.1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.easysoft.com/pub/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	a442cf6de50b0aca9cb7a984ede25e09
Source1:	DataManager.desktop
Source2:	ODBCConfig.desktop
Source3:	%{name}.png
Patch0:		%{name}-ac_fix.patch
Patch1:		%{name}-no_libnsl.patch
Patch2:		%{name}-libltdl-shared.patch
Patch3:		%{name}-trailing_backslash.patch
Patch4:		%{name}-flex.patch
Icon:		unixODBC.xpm
URL:		http://www.unixodbc.com/
#BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	readline-devel >= 4.2
#BuildRequires:	qt-devel >= 2.0
Requires(post):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildConflicts:	kdesupport-odbc
Obsoletes:	libunixODBC2

%define		_sysconfdir	/etc

%description
unixODBC is a complete, free/open, ODBC solution for UNIX/Linux.

%description -l pl
unixODBC - kompletne, darmowe/otwarte ODBC dla systemów UNIX/Linux.

%package devel
Summary:	unixODBC header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokunentacja do unixODBC
Group:		Development/Libraries
Requires:	%{name} = %{version}
Obsoletes:	libunixODBC2-devel

%description devel
unixODBC header files and development documentation.

%description devel -l pl
Pliki nag³ówkowe i dokunentacja do unixODBC.

%package static
Summary:	unixODBC static libraries
Summary(pl):	Biblioteki statyczne unixODBC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
unixODBC static libraries.

%description static -l pl
Biblioteki statyczne unixODBC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing config.guess config.sub
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-gui \
	--enable-threads \
	--enable-drivers \
	--enable-shared \
	--enable-static
# GUI requires QT2
#	--enable-gui
#	--with-qt-dir=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/System,%{_pixmapsdir}}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

#install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/System
#install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}

find doc -name Makefile\* -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# install text driver
/usr/bin/odbcinst -i -d -r <<EOF
[TXT]
Description = Text file driver
Driver = %{_libdir}/libodbctxt.so
Setup = %{_libdir}/libodbctxtS.so
EOF
# install postgresql driver
/usr/bin/odbcinst -i -d -r <<EOF
[PostgreSQL]
Description = PostgreSQL driver
Driver = %{_libdir}/libodbpsql.so
Setup = %{_libdir}/libodbpsqlS.so
EOF

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS doc/AdministratorManual doc/UserManual
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/odbc*.ini
#%%{_applnkdir}/System/*
#%%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog doc/ProgrammerManual
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%attr(644,root,root)
%{_libdir}/lib*.a

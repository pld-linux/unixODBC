Summary:	unixODBC -a complete, free/open, ODBC solution for UNIX/Linux
Summary(pl):	unixODBC
Name:		unixODBC
Version:	1.8.13
Release:	3
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	ftp://ftp.easysoft.com/pub/beta/%{name}/%{name}-%{version}.tar.gz
Source1:	DataManager.desktop
Source2:	ODBCConfig.desktop
Source3:	odbcinst.ini
Patch0:		%{name}-DESTDIR.patch
BuildRequires:	automake
#BuildRequires:	XFree86-devel
#BuildRequires:	qt-devel >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildConflicts:	kdesupport-odbc

%define		_prefix		/usr
%define		_sysconfdir	/etc

%description
unixODBC is a complete, free/open, ODBC solution for UNIX/Linux.

%package devel
Summary:	unixODBC header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokunentacja do unixODBC 
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
unixODBC header files and development documentation.

%description -l pl
Pliki nag³ówkowe i dokunentacja do unixODBC.

%package static
Summary:	unixODBC static libraries
Summary(pl):	Biblioteki statyczne unixODBC
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
unixODBC static libraries.

%description -l pl static
Biblioteki statyczne unixODBC.

%prep
%setup -q 
%patch -p1

%build
libtoolize --force
automake
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
install -d $RPM_BUILD_ROOT%{_applnkdir}/System

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/System
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf AUTHORS NEWS

find doc -name Makefile\* -exec rm {} \;

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,NEWS}.gz doc/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 size mtime)  %{_sysconfdir}/odbc*.ini
%{_applnkdir}/System/*

%files devel
%defattr(644,root,root,755)
#doc {AUTHORS,NEWS}.gz doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%attr(644,root,root) 
%{_libdir}/lib*.a

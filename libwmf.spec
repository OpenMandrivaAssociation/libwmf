%define api 0.2
%define major	7
%define libname %mklibname wmf%{api}_ %major
%define litename %mklibname wmflite%{api}_ %major
%define develname %mklibname -d wmf

Summary:	A library to convert wmf files
Name:		libwmf
Version:	0.2.8.4
Release:	25
License:	GPL
Group:		Text tools
URL:		http://sourceforge.net/projects/wvware/
Source0:	http://download.sourceforge.net/wvware/%{name}-%{version}.tar.bz2
Patch0:		libwmf-0.2.7-libwmf-config.patch
Patch1:		libwmf-0.2.8.3-CAN-2004-0941.patch
Patch2:		libwmf-0.2.8.3-CAN-2004-0990.patch
Patch3:		libwmf-0.2.8.4-intoverflow.patch
Patch4:		libwmf-0.2.8.4-CVE2007-2756.patch
Patch5:		libwmf-0.2.8.4-rh-CVE-2009-1364.diff
Patch6:		libwmf-0.2.8.4-gdk2.22.patch

BuildRequires:	expat-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(libpng15)
BuildRequires:	pkgconfig(x11)
Requires(post):	gdk-pixbuf2.0
Requires(postun): gdk-pixbuf2.0
Requires:	urw-fonts

%description
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

%package -n %{libname}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libwmf.

%package -n %{litename}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries

%description -n %{litename}
This package contains the library needed to run programs dynamically
linked with libwmflite.

%package -n %{develname}
Summary:	A library to convert wmf files. - development environment
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libwmf-devel = %{version}-%{release}
Obsoletes:	libwmf-devel < %{version}-%{release}
Obsoletes:	%{_lib}wmf0.2_7-devel < 0.2.8.4-21

%description -n %{develname}
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

Install libwmf-devel if you need to compile an application with libwmf
support.

%prep
%setup -q
%patch -p1 -b .fpons
%patch1 -p1 -b .can-2004-0941
%patch2 -p1 -b .can-2004-0990
%patch3 -p1 -b .cve-2006-3376
%patch4 -p1 -b .cve-2007-2756
%patch5 -p0 -b .CVE-2009-1364
%patch6 -p0 -b .gdk222

%build
autoreconf -fi
%configure2_5x \
	--disable-static

%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std

#remove not packaged files
find %{buildroot} -name *.la | xargs rm

mv %{buildroot}%{_prefix}/share/doc/* installed-docs

#gw no windows line endings
perl -pi -e 's/\r//' $(find installed-docs -type f )

# remove anything relevant to fonts.
rm -rf %{buildroot}%{_bindir}/libwmf-fontmap %{buildroot}%{_datadir}/libwmf

# multiarch support
%multiarch_binaries %{buildroot}%{_bindir}/libwmf-config

%files
%docdir COPYING
%{_bindir}/wmf2*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/io-wmf.*

%files -n %{libname}
%{_libdir}/libwmf-%{api}.so.%{major}*

%files -n %{litename}
%{_libdir}/libwmflite-%{api}.so.%{major}*

%files -n %{develname}
%doc CREDITS README NEWS ChangeLog
%doc installed-docs/*
%{_bindir}/libwmf-config
%{multiarch_bindir}/libwmf-config
%{_libdir}/libwmf.so
%{_libdir}/libwmflite.so
%{_includedir}/libwmf


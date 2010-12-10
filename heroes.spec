%define	name		heroes
%define	version		0.21
%define release		%mkrel 9
%define	dataversion	1.5
%define Summary		Game like Nibbles but different

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://download.sourceforge.net/heroes/%{name}-%{version}.tar.bz2
Source1:	http://download.sourceforge.net/heroes/%{name}-data-%{dataversion}.tar.bz2
Source2:	http://download.sourceforge.net/heroes/%{name}-sound-tracks-1.0.tar.bz2
Source3:	http://download.sourceforge.net/heroes/%{name}-sound-effects-1.0.tar.bz2
Source5:	%{name}-16.png
Source6:	%{name}-32.png
Source7:	%{name}-48.png
Patch0:		%{name}-0.21-debian-fixes.patch.bz2
Patch1:		heroes-0.21-fix-build-gcc4.patch.bz2
License:	GPL
Url:		http://heroes.sourceforge.net/
Group:		Games/Arcade
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gettext bison SDL-devel SDL_mixer-devel

%description
Heroes is similar to the "Tron" and "Nibbles" games of yore, but includes
many graphical improvements and new game features.  In it, you must
maneuver a small vehicle around a world and collect powerups while avoiding
obstacles, your opponents' trails, and even your own trail. Several modes
of play are available, including "get-all-the-bonuses", deathmatch, and
"squish-the-pedestrians".

%prep
%setup -q
%setup -q -D -T -a 1
%setup -q -D -T -a 2
%setup -q -D -T -a 3
%patch0 -p1
%patch1 -p1

cat <<EOF > %{name}.menu
?package(%{name}):command="%{_gamesbindir}/%{name}" \
		  icon=%{name}.png \
		  needs="x11" \
		  section="More Applications/Games/Arcade" \
		  title="Heroes"\
		  longtitle="%{Summary}" xdg="true"
EOF

cat << EOF > mandriva-%{name}.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Heroes
Comment=%{summary}
Exec=%_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%build
%configure	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--disable-debug \
		--with-sdl
%make LDFLAGS="-lm -lpthread"
    (cd %{name}-data-%{dataversion}
     %configure	--bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
     %make
    )       
for i in sound-effects sound-tracks; do
    (
    cd %{name}-$i-1.0
    %configure --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
		    
    %make
    )
done

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}
    (cd %{name}-data-%{dataversion}
     %makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}
    )
for i in sound-effects sound-tracks; do
    (
    cd %{name}-$i-1.0
    %makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}
    )
done

mv $RPM_BUILD_ROOT%{_gamesdatadir}/locale/ $RPM_BUILD_ROOT%{_datadir}/
%find_lang %{name}

install -D -m644 mandriva-%{name}.desktop $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop
install -m644 %SOURCE6 -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %SOURCE5 -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %SOURCE7 -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%if %mdkversion < 200900
%update_menus
%endif
%_install_info %name.info

%postun
%if %mdkversion < 200900
%clean_menus
%endif
%_remove_install_info %name.info

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README THANKS TODO
%{_gamesdatadir}/%{name}
%{_mandir}/man6/%{name}*
%{_gamesbindir}/%{name}*
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_infodir}/%{name}.info*


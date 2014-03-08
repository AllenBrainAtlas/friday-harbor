%
% --- set up global values such as volume size and x,y,z indices
%
global dimSize spacing

dimSize = [133,81,115];
spacing = 100;
voxelIndex = (0 : prod(dimSize) - 1)';
zIndex = floor( voxelIndex / prod(dimSize(1:2)) );
yIndex = floor( ( voxelIndex - (zIndex * prod(dimSize(1:2)))) / dimSize(1) );
xIndex = voxelIndex - yIndex * dimSize(1) - zIndex * prod(dimSize(1:2));

%
% --- read in the structures information
% 1 = structure id
% 2 = acronym
% 3 = graph_order
% 4 = red
% 5 = green
% 6 = blue
% 7 = structure path to root
% 8 = name
%
% global ST
% fid = fopen( 'ontology.txt');
% ST = textscan( fid, '%d %s %d %d %d %d %s %s', 'HeaderLines', 1, 'Delimiter', '|');
% fclose(fid);
% clear fid;

%
% --- read in the annotated voxel volume
%
fname = '../src/gridAnnotation.raw';

global Samples AN ZZ YY XX LH V2M

AN = ReadVolume( fname, 'uint16');
Samples = (AN > 0 );
AN = AN(Samples); % structure id
ZZ = zIndex(Samples); % z coordinate
YY = yIndex(Samples); % y coordinate
XX = xIndex(Samples); % x coordinate
LH = (ZZ < 58); % is left hemisphere
% 
% for p = 1:length(GO)
%     ind = find(ST{1} == AN(p));
%     GO(p) = ST{3}(ind);
%     AL(p) = ST{2}(ind);
% end

%
% --- reorder of easier intepretbility [hemisphere,graph-order,x,y,z]
%
% V2M = ZZ + YY * 1e4 + XX * 1e8 + GO * 1e12 + LH *  1e16;
% [dummy,corder] = sort(V2M);
% V2M = corder;
% clear dummy corder fname;

%-------------------------------------
% AN = AN(V2M); % structure id
% ZZ = ZZ(V2M); % z coordinate (multiply by 100 to get microns)
% YY = YY(V2M); % y coordinate (multiply by 100 to get microns)
% XX = XX(V2M); % x coordinate (multiply by 100 to get microns)
% LH = LH(V2M); % is in left hemisphere?
% GO = GO(V2M); % structure graph order
% AL = AL(V2M); % structure label
%--------------------------------------

%
% --- make structure color banner for voxels
%
% VBanner = zeros(1, length(AN), 3);
% for r = 1:length(AN)
%     ind = find ( ST{1} == AN(r) );
%     if ~isempty( ind )
%         VBanner(1,r,:) = [ST{4}(ind), ST{5}(ind), ST{6}(ind)];
%     end
% end
% VBanner = VBanner/255;

%
% --- loop through imageseries directories one-by-one
%
baseDir = '../src/raw_data';

dlist = dir(baseDir);
dlist = dlist(3:end);

% --------------------------------------------------------
IS = zeros(length(dlist),1); % image-series id
% ISP = zeros(length(dlist),1); % specimen id
% ISN = cell(length(dlist),1); % specimen name
% ISTA = cell(length(dlist),1); % injection structure acronym
% ISTI = zeros(length(dlist),1); % injection structure id
% ISTO = zeros(length(dlist),1); % injection structure order
% IPV = zeros(length(dlist),1); % injection volume
% IX = zeros(length(dlist),1); % injection x
% IY = zeros(length(dlist),1); % injection y
% IZ = zeros(length(dlist),1); % injection z
% IPI = zeros(length(dlist),1); % injection projection intensity

PD = zeros(length(dlist), length(AN)); % output density matrix
% PE = zeros(length(dlist), length(AN)); % output energy matrix
IJ = zeros(length(dlist), length(AN)); % injection matrix
MD = []; % indicates a missing data voxel


% --------------------------------------------------------


for k = 1:length(dlist)
   
%     if k > 5
%         break
%     end

    k
    
    % --- open density volume
    fname = fullfile( baseDir, dlist(k).name, 'density.raw' );
    disp( fname );
    if ~(exist(fname)==2)
        disp( 'file does not exist' )
        continue;
    end
    
    G = ReadVolume( fname, 'float32' );
%     v = G(Samples);
    PD(k,:) = G(Samples);
    
%     % --- open energy volume
%     fname = fullfile( baseDir, dlist(k).name, 'energy.raw' );
%     %disp( fname );
%     if ~exist(fname)
%         disp( 'file does not exist' )
%         continue;
%     end
%     
%     G = ReadVolume( fname, 'float32' );
%     v = G(Samples);
%     PE(k,:) = v(V2M);
    
    % -- open injection volume
    fname = fullfile( baseDir, dlist(k).name, 'injection.raw' );
    %disp( fname );
    if ~(exist(fname) == 2)
        disp( 'file does not exist' )
        continue;
    end
    
    G = ReadVolume( fname, 'float32' );
%     v = G(Samples);
    IJ(k,:) = G(Samples);
    
    % -- open meta-data file
%     fname = fullfile( baseDir, dlist(k).name, 'image_series.txt' );
%     fid = fopen( fname, 'r' );
%     ss = textscan( fid, '%d %d %s %d %s %f %d %d %d %f', 'HeaderLines', 1, 'Delimiter', '|');
%     fclose(fid);
%     clear fid;
    
    IS(k) = str2num(dlist(k).name);
%     ISP(k) = ss{2};
%     ISN(k) = ss{3};
%     ISTI(k) = ss{4};
%     ISTA(k) = ss{5};
%     IPV(k) = ss{6};
%     IX(k) = ss{7};
%     IY(k) = ss{8};
%     IZ(k) = ss{9};
%     IPI(k) = ss{10};
%     
%     ind = find(ST{1} == ISTI(k));
%     ISTO(k) = ST{3}(ind);
    
    
end    


% -- find missing data voxels and zero out voxels in matrix
MD = (PD < 0);% | PE < 0);

% ---- "-3" indicates false positive. Set to zero and use in materix
MD(PD==-3) = 0.0;% | PE==-3) = 0; 
PD(PD==-3) = 0.0;% | PE==-3) = 0;
% PE(PD==-3 | PE==-3) = 0;

PD(MD) = 0.0;
% PE(MD) = 0.0;

% --- reorder by structure ontology for intepretability
% [dummy, corder] = sort(ISTO);
% IS = IS(corder);
% ISP = ISP(corder);
% ISN = ISN(corder);
% ISTA = ISTA(corder);
% ISTI = ISTI(corder);
% ISTO = ISTO(corder);
% IPV = IPV(corder);
% IX = IX(corder);
% IY = IY(corder);
% IZ = IZ(corder);
% IPI = IPI(corder);

% PD = PD(corder,:);
% % PE = PE(corder,:);
% IJ = IJ(corder,:);
% MD = MD(corder,:);
% clear dummy corder

%
% --- make structure color banner for experiments
%
% EBanner = zeros(length(IS),1,3);
% for r = 1:length(IS)
%     ind = find( ST{1} == ISTI(r) );
%     if ~isempty( ind )
%         EBanner(r,1,:) = [ST{4}(ind), ST{5}(ind), ST{6}(ind)];
%    end
% end    
% EBanner = EBanner/255;

% -- visualize the matrix
% figure; colormap(jet(256)); imagesc(log10(PD));
% figure; colormap(jet(256)); imagesc(log10(PE));
% figure; colormap(jet(256)); imagesc(IJ); caxis([0 0.1]);
% figure; colormap(gray(2)); imagesc(MD); 
% figure; image(VBanner);
% figure; image(EBanner); 

% Save results:
save('../src/PD.hdf5', 'PD','-v7.3')
save('../src/IS.hdf5', 'IS','-v7.3')
save('../src/IJ.hdf5', 'IJ','-v7.3')
save('../src/AN.hdf5', 'AN','-v7.3')
save('../src/XX.hdf5', 'XX','-v7.3')
save('../src/YY.hdf5', 'YY','-v7.3')
save('../src/ZZ.hdf5', 'ZZ','-v7.3')
save('../src/LH.hdf5', 'LH','-v7.3')


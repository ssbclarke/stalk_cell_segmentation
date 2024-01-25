function CreateFEM()

    clc; clear all;

    I = imread('Val_1_CellProfilerProcessed.png');

    BW = im2bw(I);
    BW = imcomplement(BW);

    % find vertices

    verts = cell(1000,1);

    imshow(BW)

    hold on;

    for i=1:size(BW,1)

        for j=1:size(BW,2)

            %if it's an edge pixel and black, it's a vertex

            if i == 1 || i == size(BW,1) || j == 1 || j == size(BW,2)

                if BW(i,j) == 0

                    verts{i} = [i,j];
                    verts{j} = [i,j];

                    plot(j,i,'o')

                end

            %otherwise, see if it's a vertex by checking how many neighboring pixels are also black

            else

                count = 0;

                for m=-1:2:1

                        if(BW(i+m,j)==0)

                            count = count + 1;

                        end

                        if(BW(i,j+m)==0)

                            count = count + 1;

                        end

                end

                if count >= 3 && BW(i,j)==0

                    verts{i} = [i,j];
                    verts{j} = [i,j];

                    plot(j,i,'o')

                end
    % 
            end

        end

    end


    %% Extract internal vertex coordinates

    allverts = verts(~cellfun('isempty',verts)); % remove empty cells

    converts = cell2mat(allverts); % convert cells to matrix

    uniqverts = unique(converts(:,1:2),'rows','stable'); % extract unique rows in matrix


    % Extract only border vertices

    borderverts = zeros(size(uniqverts));

    for iu = 1:size(uniqverts)

        if uniqverts(iu,1)==1 || uniqverts(iu,2) == 1 || uniqverts(iu,1) == size(BW,1) || uniqverts(iu,2) == size(BW,2)

            borderverts(iu,1)= uniqverts(iu,1);

            borderverts(iu,2)= uniqverts(iu,2);

        end

    end

    borderverts(all(~borderverts,2),:) = [];


    % Extract only internal vertices

    uniqverts(ismember(uniqverts,borderverts,'rows'),:)=[];

    iverts = uniqverts;

    % innerverts = ismember(uniqverts,borderverts);
    % 
    % iverts=zeros(size(innerverts));
    % 
    % for inv = 1:size(innerverts)
    %     
    %     if innerverts(inv,1)==0 && innerverts(inv,2)==0
    %         
    %         iverts(inv,1)=uniqverts(inv,1);
    %         
    %         iverts(inv,2)=uniqverts(inv,2);
    %         
    %     end
    %     
    % end
    % 
    % iverts(all(~iverts,2),:)=[];


    %% Seperate cell walls at internal vertices to get separate splines 

    BWinvert = ~BW;

    for ivs = 1:length(iverts)

            if BWinvert(iverts(ivs,1),iverts(ivs,2))==1

                BWinvert(iverts(ivs,1),iverts(ivs,2))=0;

            end
    end

    [labelledBW,noofsplinz] = bwlabel(BWinvert,4);

    imshow(labelledBW)

    hold on 

    for isp = 1:noofsplinz

        [splinerow,splinecol] = find(labelledBW==isp) ; 

        splinecoord = [splinerow splinecol];

        plot(splinecol,splinerow,'o')

    end


    %% Write python file to sketch cell wall splines

    outputFolderPath = 'C:\Users\cstubbs\Documents\Research\Stephen Clarke\Github 2023-10-27\ValidationSet\Val_1\'; 

    boundaryName = 'Val_1_CellProfilerProcessed';     

    filename = sprintf('%s.py',boundaryName);       

    filename = strcat(outputFolderPath,filename);       

    fileID = fopen(filename,'w');       

    fprintf(fileID,'from sketch import *\n\n');      

    fprintf(fileID,'mdb.models[''Model-1''].ConstrainedSketch(name=''__profile__'', sheetSize=200.0)\n');       

    for isp2 = 1:noofsplinz        

        [rows,cols] = find(labelledBW==isp2) ; 

        splinecoord = [rows cols]; 

        [~,rowidx] = unique(rows);

        [~,colidx] = unique(cols);

        uniqrows = length(rowidx);

        uniqcols = length(colidx);

        if uniqrows > uniqcols

            splinecoords = splinecoord(rowidx,:);

        else

            splinecoords = splinecoord(colidx,:);

        end

        [vertidx,distance] = dsearchn(iverts,splinecoords);

        vertsidx = unique(vertidx);

        if length(vertsidx) == 1 

            vertcoord = iverts(vertsidx(1),1:2);

            splinetop = splinecoords(1,:);

            splinebottom = splinecoords(size(splinecoords,1),:);

            topcoorddist = pdist2(splinetop,vertcoord);

            bottomcoorddist = pdist2(splinebottom,vertcoord);

            if topcoorddist > bottomcoorddist

                splinecoords = [splinecoords;vertcoord];

            else

                splinecoords = [vertcoord;splinecoords];
            end

        else

            vertscoords = zeros(size(vertsidx));

            for ivx = 1:length(vertsidx)

                vertscoords(ivx,1:2) = [iverts(vertsidx(ivx),1) iverts(vertsidx(ivx),2)];

                splinetop = splinecoords(1,:);

                splinebottom = splinecoords(size(splinecoords,1),:);

                topcoorddist = pdist2(splinetop,vertscoords(ivx,1:2));

                bottomcoorddist = pdist2(splinebottom,vertscoords(ivx,1:2));

                    if topcoorddist > bottomcoorddist

                        splinecoords = [splinecoords;vertscoords(ivx,1:2)];

                    else

                        splinecoords = [vertscoords(ivx,1:2);splinecoords];

                    end

            end

        end

        fprintf(fileID,'mdb.models[''Model-1''].sketches[''__profile__''].Spline(points=(\n\t');

        formatSpec = '(%4.4f, %4.4f), ';        

        fprintf(fileID,formatSpec,splinecoords(1,1),splinecoords(1,2));

            for ic = 2:10:(size(splinecoords,1)-1)

                formatSpec = '(%4.4f, %4.4f), ';    

                fprintf(fileID,formatSpec,splinecoords(ic,1),splinecoords(ic,2));       

            end

            formatSpec = '(%4.4f, %4.4f), ';

            fprintf(fileID,formatSpec,splinecoords((size(splinecoords,1)),1),splinecoords((size(splinecoords,1)),2));

        fprintf(fileID,'\t))\n');

    end

    fprintf(fileID,'mdb.models[''Model-1''].sketches.changeKey(fromName=''__profile__'', toName=''mcells2'')\n');     

end
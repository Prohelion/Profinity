% main.m - Clean Octave/MATLAB example for Prohelion BMS data science
% Compatible with Octave 10+ and MATLAB (no Java, no extra packages)
% Public release version: improved input, error handling, and plotting

function main()
    %% --- User Input Section ---
    defaultServerUrl = 'http://127.0.0.1:18080';
    prompt = ['Enter Prohelion API server URL [' defaultServerUrl ']: '];
    serverUrl = input(prompt, 's');
    if isempty(serverUrl)
        serverUrl = defaultServerUrl;
    end
    % Basic URL validation
    if ~startsWith(serverUrl, 'http')
        error('Server URL must start with http or https.');
    end
    username = input('Enter your Prohelion API username: ', 's');
    disp('Warning: Your password will be visible as you type.');
    password = input('Enter your Prohelion API password: ', 's');

    %% --- Authentication ---
    try
        token = login(serverUrl, username, password);
        fprintf('Authenticated! Token received.\n');
    catch ME
        error('Login failed: %s', ME.message);
    end

    %% --- Fetch BMS Data ---
    try
        bmsData = fetch_bms_data(serverUrl, token);
    catch ME
        error('Failed to fetch BMS data: %s', ME.message);
    end
    disp('Top-level fields in BMS data:');
    disp(fieldnames(bmsData));

    %% --- Parse CMU Cell Voltages ---
    try
        [cmuVoltages, cmuNumbers] = get_cmu_cell_voltages(bmsData);
    catch ME
        error('Failed to parse CMU cell voltages: %s', ME.message);
    end

    %% --- Set negative voltages to zero ---
    for k = 1:numel(cmuNumbers)
        v = cmuVoltages{k};
        v(v < 0) = 0;
        cmuVoltages{k} = v;
    end

    %% --- Plotting ---
    figure;
    hold on;
    plotted = false;
    allVoltages = [];
    colorOrder = lines(numel(cmuNumbers));
    for k = 1:numel(cmuNumbers)
        v = cmuVoltages{k};
        if isempty(v) || ~isnumeric(v)
            continue;
        end
        idx = find(v > 0); % 1-based index for values > 0
        if isempty(idx)
            continue;
        end
        plot(idx, v(idx), '-o', 'DisplayName', ['CMU ' num2str(cmuNumbers(k))], 'Color', colorOrder(k,:));
        allVoltages = [allVoltages, v(idx)];
        plotted = true;
    end
    if plotted
        legend('show');
    else
        warning('No valid cell voltages to plot.');
    end
    hold off;
    xlabel('Cell Index');
    ylabel('Voltage (V)');
    title('Cell Voltages from Each CMU');
    grid on;
    % Dynamic y-limits, but clamp to [2500, 4200] if within range
    if ~isempty(allVoltages)
        minV = min([2500, min(allVoltages)]);
        maxV = max([4200, max(allVoltages)]);
        ylim([minV maxV]);
    else
        ylim([2500 4200]);
    end
end

function [cmuVoltages, cmuNumbers] = get_cmu_cell_voltages(bmsData)
%GET_CMU_CELL_VOLTAGES Parse voltages for each CMU from the BMS data struct
%   [cmuVoltages, cmuNumbers] = GET_CMU_CELL_VOLTAGES(bmsData)
    fnames = fieldnames(bmsData);
    cmuExpr = '^Cmu(\d+)Cells(\d+)to(\d+)Voltages$';
    cmuMap = containers.Map('KeyType','double','ValueType','any');
    for i = 1:numel(fnames)
        tokens = regexp(fnames{i}, cmuExpr, 'tokens');
        if ~isempty(tokens)
            cmuNum = str2double(tokens{1}{1});
            startCell = str2double(tokens{1}{2});
            voltagesStruct = bmsData.(fnames{i});
            if isKey(cmuMap, cmuNum)
                cellList = cmuMap(cmuNum);
            else
                cellList = {};
            end
            cellList{end+1} = struct('startCell', startCell, 'voltages', voltagesStruct);
            cmuMap(cmuNum) = cellList;
        end
    end
    if isempty(keys(cmuMap))
        error(['No CMU cell voltage data found in response. ', ...
            'Check if the API endpoint is correct and returns expected data.']);
    end
    cmuNumbers = sort(cell2mat(keys(cmuMap)));
    cmuVoltages = cell(1, numel(cmuNumbers));
    for k = 1:numel(cmuNumbers)
        cmuNum = cmuNumbers(k);
        cellChunks = cmuMap(cmuNum);
        [~, idx] = sort(cellfun(@(c) c.startCell, cellChunks));
        voltages = [];
        for j = idx
            vstruct = cellChunks{j}.voltages;
            vfields = fieldnames(vstruct);
            [~, vorder] = sort(cellfun(@(s) sscanf(s,'Cell%d'), vfields));
            for vi = vorder'
                val = vstruct.(vfields{vi});
                if isnumeric(val)
                    voltages = [voltages, val(:)'];
                end
            end
        end
        cmuVoltages{k} = voltages;
    end
end

function token = login(serverUrl, username, password)
%LOGIN Authenticates with the Prohelion API and returns a token.
%   token = LOGIN(serverUrl, username, password)
    loginEndpoint = '/api/v2/Users/Authenticate';
    loginUrl = [serverUrl loginEndpoint];

    if exist('OCTAVE_VERSION', 'builtin')
        % Octave: use curl
        jsonData = jsonencode(struct('username', username, 'password', password));
        jsonDataWin = strrep(jsonData, '"', '\"');
        tmpFile = tempname;
        curlCmd = sprintf('curl -s -X POST -H "Content-Type: application/json" -d "%s" "%s" -o "%s"', jsonDataWin, loginUrl, tmpFile);
        status = system(curlCmd);
        if status ~= 0
            error('curl command failed to execute.');
        end
        raw = fileread(tmpFile);
        delete(tmpFile);
        loginResponse = jsondecode(raw);
    else
        % MATLAB: use webwrite with struct
        loginData = struct('username', username, 'password', password);
        options = weboptions( ...
            'MediaType', 'application/json', ...
            'ContentType', 'json', ...
            'Timeout', 20, ...
            'RequestMethod', 'post' ...
        );
        loginResponse = webwrite(loginUrl, loginData, options);
    end

    disp('Decoded login response:');
    disp(loginResponse);

    if isfield(loginResponse, 'token')
        token = loginResponse.token;
    else
        error('No token received from server. Check your credentials and server URL.');
    end
end

function bmsData = fetch_bms_data(serverUrl, token)
%FETCH_BMS_DATA Fetches BMS data from the Prohelion API using the token.
%   bmsData = FETCH_BMS_DATA(serverUrl, token)
    bmuEndpoint = '/api/v2/Data/Prohelion%20BMU';
    bmuUrl = [serverUrl bmuEndpoint];

    if exist('OCTAVE_VERSION', 'builtin')
        % Octave: use curl for GET with Bearer token
        tmpFile = tempname;
        curlCmd = sprintf('curl -s -H "Authorization: Bearer %s" "%s" -o "%s"', token, bmuUrl, tmpFile);
        status = system(curlCmd);
        if status ~= 0
            error('curl command failed to execute.');
        end
        raw = fileread(tmpFile);
        delete(tmpFile);
        bmsData = jsondecode(raw);
    else
        % MATLAB: use webread with Bearer token
        options = weboptions( ...
            'HeaderFields', {'Authorization', ['Bearer ' token]}, ...
            'ContentType', 'json', ...
            'Timeout', 20 ...
        );
        bmsData = webread(bmuUrl, options);
    end
end

main;

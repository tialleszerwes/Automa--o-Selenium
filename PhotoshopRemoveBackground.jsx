function removeBackground()
{
    /*------------------------------------------------------------------------------------
	https://github.com/kavindupasan/batch-bg-remover-photoshop/blob/v2/remove-bg.jsx
	updated on 2020-12-13
	This scripts supports Photoshop CC 2020 and above versions.
	How to use the script: https://youtu.be/6ICVsi2pWyk
	--------------------------------------------------------------------------------------*/


	/*------------------------------------------------------------------------------------
	Configure following paramers before running the script
	--------------------------------------------------------------------------------------*/
	//Place all images needs to be processed in a folder. Add the path below.
	
	var lstFotosNaoConvertidas = [];
	//var sourceFolder = Folder("C:\\Users\\Tiall\\Downloads\\Fotos Teste Photoshop");
	
	var sourceFolder = Folder("C:\\Users\\Tiall\\Downloads\\Fotos Aprovadas");
	
	
	//Add the path of an existing folder below to save the output.
	var saveFolder = new Folder("C:\\Users\\Tiall\\Downloads\\PhotoShop feito");
	//Fill color of the background
	var colorRef = new SolidColor;
	colorRef.rgb.red = 255;
	colorRef.rgb.green = 255;
	colorRef.rgb.blue = 255;
	//Set below to true to make the background transparent.
	var isTransparent = true;
	//Set below to true to use an image as background
	var isImageBg = false;
	//If isImageBg is set to true,
	//it's required to the background image to be preopened in photohsop
	//Backdound image must be the active document
	//-----------------------------------------------------------------------------------


	//Check if it's selected to use an image as background
	if(isImageBg){
		//Store background image and a variable
		var doc_bg = app.activeDocument;
	}


	//Cheks if the source folder is null
  	if (sourceFolder != null)
  	{
	//The following line will list all files (not only image files) on the source folder.
	//If you have any non-image files (even hidden) , please see the next comment.
    	//var fileList = sourceFolder.getFiles();
	//Comment the above line and uncomment the following line to filter specific file types.
	//Try filter files types if the script fails.
	var fileList = sourceFolder.getFiles(/\.(jpg|jpeg|png|tif|psd|crw|cr2|nef|dcr|dc2|raw|heic)$/i);
  	}
  	else{
	 	 alert("No images found on source folder");
  	}

	//Now this will open every file in the file list
	//for(var a = 5249 ;a <= 5257; a++){

	for(var a = 0 ;a < fileList.length; a++){
		//Open file in photoshop    
		app.open(fileList[a]);

		if(app.activeDocument.name.toLowerCase().indexOf("fundo") == -1){

			// Acessa o documento ativo
			var doc = app.activeDocument;

			// Verifica se o documento já está no modo RGB
			if (doc.mode != DocumentMode.RGB) {
    			// Converte o documento para RGB
    			doc.changeMode(ChangeMode.RGB);
			}

			// Select subject
			var idautoCutout = stringIDToTypeID( "autoCutout" );
			var desc01 = new ActionDescriptor();
			var idsampleAllLayers = stringIDToTypeID( "sampleAllLayers" );
			desc01.putBoolean( idsampleAllLayers, false );
			try{
				executeAction( idautoCutout, desc01, DialogModes.NO );
			}
			catch(err){}

			// Invert the selection
			app.activeDocument.selection.invert();
			//Now the background is selected. Next step is to fill or clear the selection.
			if(isTransparent){
				//Make active layer a normal layer.
				try{
					activeDocument.activeLayer.isBackgroundLayer = false;
					//Make the selection transparent
					app.activeDocument.selection.clear();
				}
				catch(err){
					lstFotosNaoConvertidas.push(app.activeDocument.name)
					continue;
				}
			}
			else{
				app.activeDocument.selection.fill(colorRef);
			}

			// var selection = app.activeDocument.selection;
			var layer = app.activeDocument.activeLayer;
	
			// Verifica se a camada ativa é uma camada de fundo e a converte
			if (layer.isBackgroundLayer) {
				layer.isBackgroundLayer = false;
			}

			// Aplica a suavização das bordas (feather)
			// app.activeDocument.selection.feather(4);
	

			// Adiciona a máscara de camada
			// layer.addLayerMask();

			// Inverte a seleção e limpa a área
			// selection.invert();
			// app.activeDocument.selection.clear();
	
			//melhora a qualidade da imagem
   			// var originalLayer = app.activeDocument.activeLayer;
    		// var duplicateLayer = originalLayer.duplicate();
    		// duplicateLayer.applyHighPass(1);
    		// duplicateLayer.blendMode = BlendMode.OVERLAY;
    		// duplicateLayer.merge(); // app.activeDocument.mergeVisibleLayers();

			app.activeDocument.selection.invert();

			// addDropShadow(app);
			//Check if it's selected to use an image as background
			if(isImageBg){
				//Store main document to a variable
				var main_doc = app.activeDocument;
				//Swich to background image
				app.activeDocument = doc_bg;
				//Copy background to the main image
				app.activeDocument.activeLayer.duplicate(main_doc, ElementPlacement.PLACEATEND);
				//Switch to the main image
				app.activeDocument = main_doc;
			}
	
   	 		//realiza um TRIM Na imagem
    		app.activeDocument.trim(TrimType.TRANSPARENT);

    		//verifica as dimensões da imagem e altera o maior lado para 900
    		if(app.activeDocument.width.as('px') > app.activeDocument.height.as('px'))
    		{
        		app.activeDocument.resizeImage("880px",undefined)
    		}
    		else
			{
       			app.activeDocument.resizeImage(undefined, "880px")
    		}

    		// ajusta o tamanho do canva para 1200px X 1200px
    		app.activeDocument.resizeCanvas("1200px", "1200px", AnchorPosition.MIDDLECENTER);


			//Now the image is proccessed. Next step is saving the image.
			//Create the file name making a proper name for an URL
			var fileName = app.activeDocument.name.replace(/[^a-zA-Z0-9-._~\s]/g, '').replace(/\s+/g, '-').replace("JPG","");

			var jpgSaveOptions = new JPEGSaveOptions();
			jpgSaveOptions.quality = 12;  // A qualidade do JPG pode ser entre 0 e 12 (sendo 12 a melhor qualidade)
			jpgSaveOptions.formatOptions = FormatOptions.STANDARDBASELINE;  // Usar baseline padrão
			jpgSaveOptions.matte = MatteType.NONE;  // Sem fundo
			jpgSaveOptions.embedColorProfile = true;  // Embutir o perfil de cor (se necessário)

			// Salve a imagem no formato JPG
			app.activeDocument.saveAs(new File(saveFolder + '\\' + fileName), jpgSaveOptions, true, Extension.LOWERCASE);
		}
		// Fechar o documento sem salvar alterações adicionais (se necessário)
		app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
	}

	arquivos = ""
	for(a = 0; a < lstFotosNaoConvertidas.length; a++){
		arquivos += " " + lstFotosNaoConvertidas[a];
	}	
	alert(arquivos)
}

function addDropShadow(app) {
	var idsetd = charIDToTypeID( "setd" );
var desc677 = new ActionDescriptor();
var idnull = charIDToTypeID( "null" );
    var ref90 = new ActionReference();
    var idPrpr = charIDToTypeID( "Prpr" );
    var idLefx = charIDToTypeID( "Lefx" );
    ref90.putProperty( idPrpr, idLefx );
    var idLyr = charIDToTypeID( "Lyr " );
    var idOrdn = charIDToTypeID( "Ordn" );
    var idTrgt = charIDToTypeID( "Trgt" );
    ref90.putEnumerated( idLyr, idOrdn, idTrgt );
desc677.putReference( idnull, ref90 );
var idT = charIDToTypeID( "T   " );
    var desc678 = new ActionDescriptor();
    var idScl = charIDToTypeID( "Scl " );
    var idPrc = charIDToTypeID( "#Prc" );
    desc678.putUnitDouble( idScl, idPrc, 416.666667 );
    var idDrSh = charIDToTypeID( "DrSh" );
        var desc679 = new ActionDescriptor();
        var idenab = charIDToTypeID( "enab" );
        desc679.putBoolean( idenab, true );
        var idpresent = stringIDToTypeID( "present" );
        desc679.putBoolean( idpresent, true );
        var idshowInDialog = stringIDToTypeID( "showInDialog" );
        desc679.putBoolean( idshowInDialog, true );
        var idMd = charIDToTypeID( "Md  " );
        var idBlnM = charIDToTypeID( "BlnM" );
        var idNrml = charIDToTypeID( "Nrml" );
        desc679.putEnumerated( idMd, idBlnM, idNrml );
        var idClr = charIDToTypeID( "Clr " );
            var desc680 = new ActionDescriptor();
            var idRd = charIDToTypeID( "Rd  " );
            desc680.putDouble( idRd, 0.000000 );
            var idGrn = charIDToTypeID( "Grn " );
            desc680.putDouble( idGrn, 0.000000 );
            var idBl = charIDToTypeID( "Bl  " );
            desc680.putDouble( idBl, 0.000000 );
        var idRGBC = charIDToTypeID( "RGBC" );
        desc679.putObject( idClr, idRGBC, desc680 );
        var idOpct = charIDToTypeID( "Opct" );
        var idPrc = charIDToTypeID( "#Prc" );
        desc679.putUnitDouble( idOpct, idPrc, 56.000000 );
        var iduglg = charIDToTypeID( "uglg" );
        desc679.putBoolean( iduglg, true );
        
        // Aqui definimos a direção da sombra para baixo com um ângulo de 180 graus
        var idlagl = charIDToTypeID( "lagl" );
        var idAng = charIDToTypeID( "#Ang" );
        desc679.putUnitDouble( idlagl, idAng, 180.000000 ); // Direção para baixo, 180 graus

        var idDstn = charIDToTypeID( "Dstn" );
        var idPxl = charIDToTypeID( "#Pxl" );
        desc679.putUnitDouble( idDstn, idPxl, 13.000000 );
        
        var idCkmt = charIDToTypeID( "Ckmt" );
        desc679.putUnitDouble( idCkmt, idPxl, 6.000000 );
        
        var idblur = charIDToTypeID( "blur" );
        desc679.putUnitDouble( idblur, idPxl, 6.000000 );
        
        var idNose = charIDToTypeID( "Nose" );
        desc679.putUnitDouble( idNose, idPrc, 0.000000 );
        
        var idAntA = charIDToTypeID( "AntA" );
        desc679.putBoolean( idAntA, false );
        
        var idTrnS = charIDToTypeID( "TrnS" );
            var desc681 = new ActionDescriptor();
            var idNm = charIDToTypeID( "Nm  " );
            desc681.putString( idNm, "Linear" );
        var idShpC = charIDToTypeID( "ShpC" );
        desc679.putObject( idTrnS, idShpC, desc681 );
        
        var idlayerConceals = stringIDToTypeID( "layerConceals" );
        desc679.putBoolean( idlayerConceals, true );
    var idDrSh = charIDToTypeID( "DrSh" );
    desc678.putObject( idDrSh, idDrSh, desc679 );
var idLefx = charIDToTypeID( "Lefx" );
desc677.putObject( idT, idLefx, desc678 );
executeAction( idsetd, desc677, DialogModes.NO );
}



removeBackground();
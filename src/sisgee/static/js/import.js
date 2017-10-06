/****************************************************************************************************************************************/
/*** Diemp										*/
/*** Autor					: Iury Amorim		*/
/*** Data de Criação		: 05/10/2016		*/
/*** Data de Modificação	: 05/10/2016		*/
/************************************************/

/****************************************************************************************************************************************/ 
var oImport = {
	jqThis : null
	
	, Carregar: function () {
		var _this = this;

		_this.jqThis = jQuery('#jqImport');
		if (_this.jqThis.length){             
			_this.CarregarEventos();
		}
	}
	, CarregarEventos: function () {
		var _this = this;
		jQuery('.jqEnviar').on('click' , function () { _this.CallLoading(this);});
	}
	, CallLoading: function () {
		jQuery(".jqLoading").removeClass("hide");
	}
};
/****************************************************************************************************************************************/ 
jQuery(window).load(function () {
	oImport.Carregar();
});
/****************************************************************************************************************************************/
function autosave (evn) {
	// console.log(board);
	// console.log($('.container').attr('board_id'));
	const boardId = $('.container').attr('board_id');
	$.ajax({
		type: 'POST',
		dataType: 'json',
		contentType: 'application/json',
		url: 'http://0.0.0.0:8080/api/v1/boards/' + boardId,
		data: JSON.stringify(board),
		success: function (resp) {
			// console.log(resp);
		},
		error: function (error) {
			// console.log(error);
		}
	});

}
$(window).on('load', function () {
	$('.save').on('click', autosave);
});
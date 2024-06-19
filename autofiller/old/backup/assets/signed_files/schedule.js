jQuery(function ($) {
    $("#schedule-save").on("click", function () {
        if (CheckTimeInterval()) {
            $.ajax({
                type: "POST",
                url: '/ajax/update_time_interval.php',
                data: $("#timeIntervalForm").serialize(),
                success: function(data) {
                    if ('' == data) {
                        $("#event-item-msg").html('<div class="alert alert-success" role="alert">Расписание успешно создано.</div>');
                    } else {
                        $("#event-item-msg").html('<div class="alert alert-danger" role="alert">'+data+'</div>');
                    }
                }
            });
        }
    });

    // Чекбоксы в таблице записи на коворкинг
    $(".td-free .form-check-input").on("change", function () {
		hourLimit = $(this).closest("table").data("hourLimit") || 4;
        //console.log($(this).prop("checked"));
        let id = $(this).val();
        let curr_label = $(this).next('label').html();

        if ($(this).prop("checked")) { // забронировано
            if (1 == curr_label) {
                $(this).closest('td').removeClass('td-green');
                $(this).closest('td').addClass('td-red');
            }

            $(".td-busy").each(function () { // занято
                if (id == $(this).data('id')) {
                    $(this).html(+$(this).html() + 1);
                }
            });

            $(this).next('label').html(+curr_label - 1); // свободно
        } else {
            if (0 == curr_label) {
                $(this).closest('td').removeClass('td-red');
                $(this).closest('td').addClass('td-green');
            }

            $(".td-busy").each(function () {
                if (id == $(this).data('id')) { // занято
                    $(this).html(+$(this).html() - 1);
                }
            });

            $(this).next('label').html(+curr_label + 1); // свободно
        }

        if (hourLimit <= $(".td-free .form-check-input:checked").length) {
            $(".td-free.td-green .form-check-input:not(:checked)").prop("disabled", true);
        } else {
            $(".td-free.td-green .form-check-input:not(:checked)").prop("disabled", false);
        }
    });

    $("#make-reservation").on("click", function () {
        if (CheckUserClick()) {
            $.ajax({
                type: "POST",
                url: '/ajax/add_user_click.php',
                data: $("#coworkingSignUpForm").serialize(),
                success: function(data) {
                    if ('' == data) {
                        // $(".tr-free .form-check-input").prop("disabled", true);
                        // $(".event-survey").remove();
                        // $(".schedule-save-btn").remove();
                        // $("#schedule-msg").html('<div class="alert alert-success" role="alert">Вы записаны в коворкинг.</div>');
                        location.reload();
                    } else {
                        $("#schedule-msg").html('<div class="alert alert-danger" role="alert">'+data+'</div>');
                    }
                }
            });
        }
    });
	if(!!$("#lockerCheck"))
	{
		$("#lockerCheck").change(function() {
			if(this.checked)
				$("#lockerRightsBlock").show();
			else
				$("#lockerRightsBlock").hide();
		});
		$("#lockerRightsBlock")
	}
});

function CheckUserClick() {
	hourLimit = $(".tr-free").closest("table").data("hourLimit") || 4;
    var result = true;
    $('.alert').remove();

    if (0 == $(".td-free .form-check-input:checked").length || hourLimit < $(".td-free .form-check-input:checked").length) {
        result = false;
        $("#schedule-msg").html('<div class="alert alert-danger" role="alert">Неверное количество выбранных свободных мест.</div>');
    }

    if ($(".event-survey").data("showSurvey") && (0 == $(".target-survey .form-check-input:checked").length || 0 == $(".equipment-survey .form-check-input:checked").length)) {
        result = false;
        $("#survey-msg").html('<div class="alert alert-danger" role="alert">Ответьте на вопросы.</div>');
    }
	
	if($('#lockerCheck').is(':checked') && !$('#lockerRights').is(':checked'))
	{
        result = false;
        $("#survey-msg").append('<div class="alert alert-danger" role="alert">Необходимо принять правила использования шкафчиков</div>');
    }

    return result;
}

function CheckTimeInterval() {
    var result = true;
    $('.alert').remove();

    $(".form-time-interval").each(function (index) {
        let start = parseInt($("#selectHourBegin"+(index+1)).val());
        let finish = parseInt($("#selectHourEnd"+(index+1)).val());
        let memeber_count = parseInt($("#inputMembers"+(index+1)).val());

        if (start >= finish) {
            result = false;
            $(this).after('<div class="alert alert-danger" role="alert">Временной интервал задан неверно.</div>');
        }

        if (0 >= memeber_count) {
            result = false;
            $(this).after('<div class="alert alert-danger" role="alert">Количество участников должно быть больше 0.</div>');
        }
    });

    return result;
}
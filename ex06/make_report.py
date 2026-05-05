import sys
import config
import analytics
import logging

def generate_report(data, predictions):
    logging.debug("Generating report")
    analytics_obj = analytics.Analytics(data)
    
    heads, tails = analytics_obj.counts()
    head_prob, tail_prob = analytics_obj.fractions(heads, tails)
    
    pred_heads = sum(1 for p in predictions if p[0] == 1)
    pred_tails = sum(1 for p in predictions if p[1] == 1)
    
    report = config.report_template.format(
        num_observations=len(data),
        heads=heads,
        tails=tails,
        head_prob=head_prob,
        tail_prob=tail_prob,
        num_steps=config.num_of_steps,
        head_forecast=pred_heads,
        tail_forecast=pred_tails
    )
    
    logging.debug("Report generated successfully")
    return report

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 make_report.py <file_path>")
        logging.error("Incorrect number of arguments")
        sys.exit(1)
    
    try:
        research = analytics.Research(sys.argv[1])
        data = research.file_reader()
        
        analytics_obj = analytics.Analytics(data)
        
        predictions = analytics_obj.predict_random(config.num_of_steps)
        
        report = generate_report(data, predictions)
        
        if analytics_obj.save_file(report, "report", "txt"):
            print("Success\n")
            print("Content:")
            print(report)
            research.send_to_telegram("Success")
            logging.info("Report created and Telegram notification sended")
        else:
            print("Error")
            research.send_to_telegram("Error")
            logging.error("Failed to save report")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        research = analytics.Research("dummy_path")
        research.send_to_telegram("The report not created by error")
        logging.error(f"Error: {e}")
        sys.exit(1)